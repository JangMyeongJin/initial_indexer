# initial_indexer

## 주요 기능

- **한글 형태소 분석**: KoNLPy를 사용한 정확한 한국어 형태소 분석
- **다양한 분석기 지원**: Okt, Komoran, Hannanum, Kkma, Mecab 지원
- **한글 초성 추출**: 한글 텍스트에서 초성을 자동으로 추출
- **OpenSearch 연동**: 기존 인덱스에서 문장 데이터 추출
- **벌크 색인**: 효율적인 대량 데이터 색인
- **품사 필터링**: 원하는 품사만 선택적으로 추출 가능

## 주의사항

1. OpenSearch 2.19.0 버전이 필요합니다.
2. Python 3.8 이상 버전이 필요합니다.


## 주요 클래스

### KoreanMorphemeAnalyzer
- `extract_words_from_sentence(sentence, pos_filter)`: 문장에서 형태소 분석을 통해 단어 추출
- `_is_valid_korean_word(word)`: 유효한 한글 단어 여부 확인

### KoreanChoseongExtractor
- `extract_choseong(text)`: 한글 텍스트에서 초성 추출
- `is_korean_word(text)`: 한글 단어 여부 확인

### OpenSearchWordIndexer
- `extract_words_from_index()`: 소스 인덱스에서 문장 추출 및 형태소 분석
- `index_words_to_auto_search()`: 단어들을 auto-search 인덱스에 색인
- `process_words_from_source_index()`: 전체 프로세스 실행

## 필요한 패키지 설치:
```bash
pip install -r requirements.txt