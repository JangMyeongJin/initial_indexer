from initial_test import OpenSearchWordIndexer, KoreanChoseongExtractor

def example_usage():
    """사용 예제"""
    
    # 1. 초성 추출 테스트
    print("=== 초성 추출 테스트 ===")
    extractor = KoreanChoseongExtractor()
    
    test_words = ["안녕하세요", "파이썬", "프로그래밍", "한글", "컴퓨터"]
    for word in test_words:
        choseong = extractor.extract_choseong(word)
        print(f"단어: {word} -> 초성: {choseong}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. OpenSearch 연결 및 색인 예제
    print("=== OpenSearch 색인 예제 ===")
    
    # OpenSearch 연결 설정 (실제 환경에 맞게 수정)
    indexer = OpenSearchWordIndexer(
        host='localhost',
        port=9200,
        username=None,  # 보안 설정 시 사용자명
        password=None,  # 보안 설정 시 비밀번호
        use_ssl=False   # SSL 사용 여부
    )
    
    # 소스 인덱스에서 단어 추출 및 auto-search 인덱스에 색인
    try:
        indexer.process_words_from_source_index(
            source_index='your-source-index',  # 실제 소스 인덱스명
            word_field='word',                 # 단어 필드명
            target_index='auto-search'
        )
        print("색인 완료!")
        
    except Exception as e:
        print(f"오류 발생: {e}")

def test_with_sample_data():
    """샘플 데이터로 테스트"""
    print("=== 샘플 데이터 테스트 ===")
    
    # 샘플 단어 데이터
    sample_words = [
        {"word": "안녕하세요"},
        {"word": "파이썬"},
        {"word": "프로그래밍"},
        {"word": "한글"},
        {"word": "컴퓨터"},
        {"word": "데이터베이스"},
        {"word": "알고리즘"},
        {"word": "네트워크"}
    ]
    
    extractor = KoreanChoseongExtractor()
    
    print("추출된 단어와 초성:")
    for item in sample_words:
        word = item['word']
        choseong = extractor.extract_choseong(word)
        print(f"  {word} -> {choseong}")

if __name__ == "__main__":
    # 샘플 데이터 테스트
    test_with_sample_data()
    
    print("\n" + "="*50 + "\n")
    
    # 실제 OpenSearch 사용 예제 (주석 처리)
    # example_usage() 
