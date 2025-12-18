# movies.json의 genres를 char가 아닌 list 형태로 변환하는 코드

import json

file_path = 'movies/fixtures/movies.json' # 경로 확인 필요

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    fields = item['fields']
    # 문자열 "[1, 2]"를 실제 리스트 [1, 2]로 변환
    if isinstance(fields.get('genres'), str):
        fields['genres'] = json.loads(fields['genres'])
    
    # backdrop_paths도 문자열이라면 함께 변환
    if isinstance(fields.get('backdrop_paths'), str):
        fields['backdrop_paths'] = json.loads(fields['backdrop_paths'])

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("JSON 파일 수정 완료!")