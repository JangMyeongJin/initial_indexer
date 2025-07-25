from initial_test import KoreanMorphemeAnalyzer, KoreanChoseongExtractor

def test_morpheme_analysis():
    """형태소 분석 기능 테스트"""
    print("=== 형태소 분석 테스트 ===")
    
    # 테스트 문장들
    test_sentences = [
        "안녕하세요 오늘 날씨가 정말 좋네요",
        "파이썬으로 프로그래밍을 배우고 있습니다",
        "한국어 자연어 처리는 매우 흥미로운 분야입니다",
        "컴퓨터 과학과 인공지능 기술이 발전하고 있습니다",
        "데이터 분석과 머신러닝 알고리즘을 공부하고 있어요"
    ]
    
    # Okt 형태소 분석기 테스트
    print("\n--- Okt 형태소 분석기 ---")
    okt_analyzer = KoreanMorphemeAnalyzer('okt')
    
    for sentence in test_sentences:
        print(f"\n문장: {sentence}")
        words = okt_analyzer.extract_words_from_sentence(sentence, ['Noun', 'Verb', 'Adjective'])
        print(f"추출된 단어: {words}")
    
    # Komoran 형태소 분석기 테스트
    print("\n--- Komoran 형태소 분석기 ---")
    komoran_analyzer = KoreanMorphemeAnalyzer('komoran')
    
    for sentence in test_sentences:
        print(f"\n문장: {sentence}")
        words = komoran_analyzer.extract_words_from_sentence(sentence, ['NNP', 'NNG', 'VV', 'VA'])
        print(f"추출된 단어: {words}")

def test_choseong_extraction():
    """초성 추출 테스트"""
    print("\n=== 초성 추출 테스트 ===")
    
    extractor = KoreanChoseongExtractor()
    
    test_words = ["안녕하세요", "파이썬", "프로그래밍", "한국어", "컴퓨터", "데이터", "알고리즘"]
    
    for word in test_words:
        choseong = extractor.extract_choseong(word)
        print(f"단어: {word} -> 초성: {choseong}")

def test_complete_pipeline():
    """완전한 파이프라인 테스트"""
    print("\n=== 완전한 파이프라인 테스트 ===")
    
    # 샘플 문장 데이터
    sample_sentences = [
        "안녕하세요 오늘 날씨가 정말 좋네요",
        "파이썬으로 프로그래밍을 배우고 있습니다",
        "한국어 자연어 처리는 매우 흥미로운 분야입니다"
    ]
    
    morpheme_analyzer = KoreanMorphemeAnalyzer('okt')
    choseong_extractor = KoreanChoseongExtractor()
    
    all_words = []
    
    for sentence in sample_sentences:
        print(f"\n문장: {sentence}")
        
        # 1. 형태소 분석으로 단어 추출
        words = morpheme_analyzer.extract_words_from_sentence(sentence, ['Noun', 'Verb', 'Adjective'])
        print(f"추출된 단어: {words}")
        
        # 2. 각 단어에 대해 초성 추출
        for word in words:
            choseong = choseong_extractor.extract_choseong(word)
            word_data = {
                'word': word,
                'choseong': choseong,
                'word_length': len(word),
                'source_sentence': sentence
            }
            all_words.append(word_data)
            print(f"  {word} -> {choseong}")
    
    # 3. 중복 제거
    unique_words = {}
    for word_data in all_words:
        word = word_data['word']
        if word not in unique_words:
            unique_words[word] = word_data
    
    print(f"\n=== 최종 결과 ===")
    print(f"총 {len(unique_words)}개의 고유한 단어가 추출되었습니다:")
    
    for word_data in unique_words.values():
        print(f"  {word_data['word']} (초성: {word_data['choseong']}, 길이: {word_data['word_length']})")

def test_different_analyzers():
    """다양한 형태소 분석기 비교 테스트"""
    print("\n=== 다양한 형태소 분석기 비교 ===")
    
    test_sentence = "파이썬으로 프로그래밍을 배우고 있습니다"
    
    analyzers = ['okt', 'komoran', 'hannanum', 'kkma']
    
    for analyzer_type in analyzers:
        try:
            analyzer = KoreanMorphemeAnalyzer(analyzer_type)
            words = analyzer.extract_words_from_sentence(test_sentence, ['Noun', 'Verb', 'Adjective'])
            print(f"{analyzer_type.upper()}: {words}")
        except Exception as e:
            print(f"{analyzer_type.upper()}: 오류 발생 - {e}")

if __name__ == "__main__":
    # 형태소 분석 테스트
    test_morpheme_analysis()
    
    # 초성 추출 테스트
    test_choseong_extraction()
    
    # 완전한 파이프라인 테스트
    test_complete_pipeline()
    
    # 다양한 분석기 비교 테스트
    test_different_analyzers() 