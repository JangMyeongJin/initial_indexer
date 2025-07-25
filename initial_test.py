import json
import re
from opensearchpy import OpenSearch
from typing import List, Dict, Any
import logging
from konlpy.tag import Okt, Komoran, Hannanum, Kkma, Mecab

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KoreanMorphemeAnalyzer:
    """한국어 형태소 분석기"""
    
    def __init__(self, analyzer_type: str = 'okt'):
        """
        형태소 분석기 초기화
        analyzer_type: 'okt', 'komoran', 'hannanum', 'kkma', 'mecab' 중 선택
        """
        self.analyzer_type = analyzer_type
        self.analyzer = self._initialize_analyzer(analyzer_type)
        
    def _initialize_analyzer(self, analyzer_type: str):
        """형태소 분석기 초기화"""
        try:
            if analyzer_type == 'okt':
                return Okt()
            elif analyzer_type == 'komoran':
                return Komoran()
            elif analyzer_type == 'hannanum':
                return Hannanum()
            elif analyzer_type == 'kkma':
                return Kkma()
            elif analyzer_type == 'mecab':
                return Mecab()
            else:
                logger.warning(f"지원하지 않는 분석기 타입: {analyzer_type}. Okt를 사용합니다.")
                return Okt()
        except Exception as e:
            logger.error(f"형태소 분석기 초기화 실패: {e}. Okt를 사용합니다.")
            return Okt()
    
    def extract_words_from_sentence(self, sentence: str, pos_filter: List[str] = None) -> List[str]:
        """
        문장에서 단어를 추출합니다.
        
        Args:
            sentence: 분석할 문장
            pos_filter: 포함할 품사 리스트 (예: ['Noun', 'Verb', 'Adjective'])
                        None이면 모든 품사 포함
        
        Returns:
            추출된 단어 리스트
        """
        if not sentence or not sentence.strip():
            return []
        
        words = []
        
        try:
            # 영어 단어 추출 (형태소 분석 없이)
            english_words = self._extract_english_words(sentence)
            words.extend(english_words)
            
            # 한글 단어 추출 (형태소 분석)
            korean_words = self._extract_korean_words(sentence, pos_filter)
            words.extend(korean_words)
            
            return list(set(words))  # 중복 제거
            
        except Exception as e:
            logger.error(f"단어 추출 중 오류 발생: {e}")
            return []
    
    def _extract_english_words(self, sentence: str) -> List[str]:
        """영어 단어를 추출합니다."""
        import re
        
        # 영어 단어 패턴 (알파벳으로만 구성된 2글자 이상의 단어)
        english_pattern = re.compile(r'\b[a-zA-Z]{2,}\b')
        english_words = english_pattern.findall(sentence)
        
        # 유효한 영어 단어만 필터링
        valid_english_words = []
        for word in english_words:
            if self._is_valid_english_word(word):
                valid_english_words.append(word.lower())  # 소문자로 변환
        
        return valid_english_words
    
    def _extract_korean_words(self, sentence: str, pos_filter: List[str] = None) -> List[str]:
        """한글 단어를 형태소 분석을 통해 추출합니다."""
        try:
            # 형태소 분석 수행
            if self.analyzer_type == 'okt':
                morphs = self.analyzer.pos(sentence, norm=True, stem=True)
            else:
                morphs = self.analyzer.pos(sentence)
            
            # 품사 필터링 및 단어 추출
            words = []
            for word, pos in morphs:
                # 품사 필터 적용
                if pos_filter is None or pos in pos_filter:
                    # 한글 단어만 포함
                    if self._is_valid_korean_word(word):
                        words.append(word)
            
            return words
            
        except Exception as e:
            logger.error(f"한글 형태소 분석 중 오류 발생: {e}")
            return []
    
    def _is_valid_korean_word(self, word: str) -> bool:
        """유효한 한글 단어인지 확인"""
        if not word or len(word) < 2:  # 2글자 미만 제외
            return False
        
        # 한글이 포함되어 있는지 확인
        korean_pattern = re.compile(r'[가-힣]')
        if not korean_pattern.search(word):
            return False
        
        # 특수문자나 숫자만으로 구성된 경우 제외
        if re.match(r'^[^가-힣a-zA-Z]*$', word):
            return False
        
        return True

    def _is_valid_english_word(self, word: str) -> bool:
        """유효한 영어 단어인지 확인"""
        if not word or len(word) < 2:  # 2글자 미만 제외
            return False
        
        # 알파벳으로만 구성되어 있는지 확인
        if not word.isalpha():
            return False
        
        # 너무 긴 단어 제외 (50글자 이상)
        if len(word) > 50:
            return False
        
        return True

class KoreanChoseongExtractor:
    """한글 초성 추출기"""
    
    # 한글 초성 매핑
    CHOSEONG_MAP = {
        'ㄱ': '가', 'ㄲ': '까', 'ㄴ': '나', 'ㄷ': '다', 'ㄸ': '따',
        'ㄹ': '라', 'ㅁ': '마', 'ㅂ': '바', 'ㅃ': '빠', 'ㅅ': '사',
        'ㅆ': '싸', 'ㅇ': '아', 'ㅈ': '자', 'ㅉ': '짜', 'ㅊ': '차',
        'ㅋ': '카', 'ㅌ': '타', 'ㅍ': '파', 'ㅎ': '하'
    }
    
    @staticmethod
    def extract_choseong(text: str) -> str:
        """한글 텍스트에서 초성을 추출합니다. 영어는 그대로 반환합니다."""
        if not text:
            return ""
        
        # 영어 단어인지 확인
        if text.isalpha() and text.isascii():
            return text.lower()  # 영어는 소문자로 반환
        
        # 한글 초성 추출
        choseong = ""
        for char in text:
            if '가' <= char <= '힣':  # 한글 유니코드 범위
                # 한글 유니코드에서 초성 계산
                unicode_val = ord(char)
                if 44032 <= unicode_val <= 55203:  # 한글 음절 범위
                    choseong_code = (unicode_val - 44032) // 588
                    choseong_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
                    choseong += choseong_list[choseong_code]
                else:
                    choseong += char
            else:
                choseong += char
        
        return choseong
    
    @staticmethod
    def is_korean_word(text: str) -> bool:
        """텍스트가 한글 단어인지 확인합니다."""
        if not text:
            return False
        
        # 한글이 포함되어 있는지 확인
        korean_pattern = re.compile(r'[가-힣]')
        return bool(korean_pattern.search(text))

class OpenSearchWordIndexer:
    """OpenSearch 단어 색인기"""
    
    def __init__(self, host: str = 'localhost', port: int = 9200, 
                 username: str = None, password: str = None,
                 morpheme_analyzer_type: str = 'okt', use_ssl: bool = False):
        """OpenSearch 클라이언트 초기화"""
        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port, 'scheme': 'https'}],
            http_auth=(username, password),
            use_ssl=use_ssl,
            verify_certs=False
        )
        self.choseong_extractor = KoreanChoseongExtractor()
        self.morpheme_analyzer = KoreanMorphemeAnalyzer(morpheme_analyzer_type)
    
    def extract_words_from_index(self, source_index: str, sentence_fields: List[str] = ['sentence'], 
                                pos_filter: List[str] = None) -> List[Dict[str, Any]]:
        """
        소스 인덱스에서 문장 데이터를 추출하고 형태소 분석을 통해 단어를 추출합니다.
        
        Args:
            source_index: 소스 인덱스명
            sentence_fields: 문장이 저장된 필드명 리스트 (예: ['title', 'content', 'description'])
            pos_filter: 포함할 품사 리스트 (예: ['Noun', 'Verb', 'Adjective'])
        """
        words = []
        processed_sentences = 0
        
        try:
            # 스크롤 검색으로 모든 문서를 가져옴
            response = self.client.search(
                index=source_index,
                body={
                    "size": 100,
                    "query": {"match_all": {}},
                    "_source": sentence_fields
                },
                scroll='10m'
            )
            
            scroll_id = response['_scroll_id']
            hits = response['hits']['hits']
            
            while hits:
                for hit in hits:
                    source = hit['_source']
                    
                    # 여러 필드에서 문장 추출
                    for field in sentence_fields:
                        if field in source and source[field]:
                            sentence = source[field]
                            processed_sentences += 1
                            
                            # 형태소 분석을 통해 단어 추출
                            extracted_words = self.morpheme_analyzer.extract_words_from_sentence(
                                sentence, pos_filter
                            )
                            
                            # 각 단어에 대해 초성 정보 추가
                            for word in extracted_words:
                                words.append({
                                    'word': word,
                                    'choseong': self.choseong_extractor.extract_choseong(word)
                                })
                
                try:
                    # 다음 배치 가져오기
                    response = self.client.scroll(
                        body={
                            "scroll_id": scroll_id,
                            "scroll": "10m"
                        }
                    )
                    hits = response['hits']['hits']
                except Exception as scroll_error:
                    logger.warning(f"스크롤 중 오류 발생: {scroll_error}")
                    break
            
            # 스크롤 정리
            try:
                self.client.clear_scroll(body={"scroll_id": scroll_id})
            except:
                pass
            
            logger.info(f"총 {processed_sentences}개의 문장을 처리하여 {len(words)}개의 한글 단어를 추출했습니다.")
            return words
            
        except Exception as e:
            logger.error(f"단어 추출 중 오류 발생: {e}")
            raise
    
    def index_words_to_auto_search(self, words: List[Dict[str, Any]], 
                                  target_index: str = 'auto_search'):
        """단어들을 auto-search 인덱스에 색인합니다."""
        if not words:
            logger.warning("색인할 단어가 없습니다.")
            return
        
        try:
            # 벌크 색인을 위한 문서 준비
            bulk_data = []
            for word_data in words:
                # 인덱스 액션
                bulk_data.append({
                    "index": {
                        "_index": target_index,
                        "_id": word_data['word']
                    }
                })
                
                # 문서 데이터
                doc_data = {
                    "id": word_data['word'],
                    "word": word_data['word'],
                    "initial": word_data['choseong']
                }
                
                # source_sentence가 있으면 추가
                if 'source_sentence' in word_data:
                    doc_data["source_sentence"] = word_data['source_sentence']
                
                bulk_data.append(doc_data)
            
            # 벌크 색인 실행
            if bulk_data:
                print(bulk_data)
                response = self.client.bulk(body=bulk_data, refresh=True)
                
                # 결과 확인
                if response.get('errors'):
                    logger.error("벌크 색인 중 일부 오류 발생")
                    for item in response['items']:
                        if 'index' in item and item['index'].get('error'):
                            logger.error(f"오류: {item['index']['error']}")
                else:
                    logger.info(f"총 {len(words)}개의 단어를 성공적으로 색인했습니다.")
                
        except Exception as e:
            logger.error(f"색인 중 오류 발생: {e}")
            raise
    
    def process_words_from_source_index(self, source_index: str, sentence_fields: List[str] = ['title'],
                                       target_index: str = 'auto-search', pos_filter: List[str] = None):
        """
        소스 인덱스에서 문장을 추출하여 형태소 분석을 통해 단어를 추출하고 auto-search 인덱스에 색인하는 전체 프로세스
        
        Args:
            source_index: 소스 인덱스명
            sentence_fields: 문장이 저장된 필드명 리스트 (예: ['title', 'content', 'description'])
            target_index: 대상 인덱스명
            pos_filter: 포함할 품사 리스트 (예: ['Noun', 'Verb', 'Adjective'])
        """
        try:
            # 1. 인덱스에서 문장 추출 및 형태소 분석
            logger.info(f"'{source_index}' 인덱스에서 문장 추출 및 형태소 분석 중...")
            words = self.extract_words_from_index(source_index, sentence_fields, pos_filter)
            
            # 2. 인덱스에 색인
            if words:
                logger.info(f"'{target_index}' 인덱스에 색인 중...")
                self.index_words_to_auto_search(words, target_index)
                logger.info("처리 완료!")
            else:
                logger.warning("처리할 단어가 없습니다.")
                
        except Exception as e:
            logger.error(f"전체 프로세스 중 오류 발생: {e}")
            raise

def main():
    """메인 실행 함수"""
    # OpenSearch 연결 설정
    # 실제 환경에 맞게 수정하세요
    host = 'localhost'
    port = 9200
    username = None  # 보안이 설정된 경우 사용자명
    password = None  # 보안이 설정된 경우 비밀번호
    use_ssl = False  # SSL 사용 여부
    
    # 소스 인덱스 설정
    source_index = 'project'  # 실제 소스 인덱스명으로 변경
    sentence_fields = ['title', 'body', 'stack']  # 여러 필드 지정
    
    try:
        # OpenSearch 클라이언트 초기화
        indexer = OpenSearchWordIndexer(
            host='localhost',
            port=9200,
            username='admin',
            password='Clush13568!',
            use_ssl=False
        )
        
        # 전체 프로세스 실행
        indexer.process_words_from_source_index(
            source_index=source_index,
            sentence_fields=sentence_fields,  # 리스트로 전달
            target_index='auto_search',
            pos_filter=['Noun', 'Verb', 'Adjective']  # 명사, 동사, 형용사만 추출
        )
        
    except Exception as e:
        logger.error(f"프로그램 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
