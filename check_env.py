"""
Google Sheets 환경변수 진단 스크립트
Render에 배포하여 환경변수 상태 확인
"""

import os
import json

print("=" * 70)
print("🔍 Google Sheets 환경변수 진단")
print("=" * 70)

# 1. GOOGLE_SHEETS_CREDENTIALS 확인
print("\n1️⃣ GOOGLE_SHEETS_CREDENTIALS 확인")
print("-" * 70)

creds = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
if not creds:
    print("❌ 환경변수가 설정되지 않았습니다!")
    print("\nRender 대시보드에서 확인하세요:")
    print("   Dashboard → Environment → GOOGLE_SHEETS_CREDENTIALS")
else:
    print(f"✅ 환경변수 존재")
    print(f"   길이: {len(creds)} characters")
    print(f"   첫 100자: {creds[:100]}...")
    print(f"   마지막 100자: ...{creds[-100:]}")
    
    # JSON 파싱 테스트
    print("\n2️⃣ JSON 파싱 테스트")
    print("-" * 70)
    try:
        data = json.loads(creds)
        print("✅ JSON 파싱 성공!")
        print(f"   type: {data.get('type')}")
        print(f"   project_id: {data.get('project_id')}")
        print(f"   client_email: {data.get('client_email')}")
        print(f"   private_key 존재: {'✅' if 'private_key' in data else '❌'}")
        
        # 필수 필드 확인
        print("\n3️⃣ 필수 필드 확인")
        print("-" * 70)
        required = ['type', 'project_id', 'private_key', 'client_email', 
                   'private_key_id', 'auth_uri', 'token_uri']
        missing = [f for f in required if f not in data]
        
        if missing:
            print(f"❌ 누락된 필드: {missing}")
        else:
            print("✅ 모든 필수 필드 존재")
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 실패!")
        print(f"   에러: {e}")
        print(f"\n문제 진단:")
        
        # 일반적인 JSON 에러 패턴 체크
        if creds.startswith('"') or creds.startswith("'"):
            print("   ⚠️ JSON 문자열이 따옴표로 시작합니다")
            print("   → Render 환경변수에서 바깥쪽 따옴표를 제거하세요")
        
        if '\\\\n' in creds:
            print("   ⚠️ private_key의 \\n이 이중 이스케이프되었습니다")
            print("   → \\\\n을 \\n으로 수정하세요")
        
        if creds.count('{') != creds.count('}'):
            print(f"   ⚠️ 중괄호 불일치: {{ {creds.count('{')}개, }} {creds.count('}')}개")
            print("   → JSON 구조를 확인하세요")

# 4. GOOGLE_SHEETS_SPREADSHEET_ID 확인
print("\n4️⃣ GOOGLE_SHEETS_SPREADSHEET_ID 확인")
print("-" * 70)

sheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
if not sheet_id:
    print("❌ 환경변수가 설정되지 않았습니다!")
else:
    print(f"✅ Spreadsheet ID: {sheet_id}")
    
    # ID 형식 검증 (일반적으로 44자)
    if len(sheet_id) < 40:
        print(f"⚠️ ID가 너무 짧습니다 (일반적으로 44자)")
    elif len(sheet_id) > 50:
        print(f"⚠️ ID가 너무 깁니다")
    else:
        print(f"✅ ID 길이 적절 ({len(sheet_id)}자)")

# 5. 라이브러리 확인
print("\n5️⃣ 필수 라이브러리 확인")
print("-" * 70)

try:
    import gspread
    print(f"✅ gspread: {gspread.__version__}")
except ImportError:
    print("❌ gspread가 설치되지 않았습니다")
    print("   → requirements.txt에 'gspread' 추가")

try:
    from google.oauth2.service_account import Credentials
    print("✅ google-auth: 설치됨")
except ImportError:
    print("❌ google-auth가 설치되지 않았습니다")
    print("   → requirements.txt에 'google-auth' 추가")

try:
    from oauth2client.service_account import ServiceAccountCredentials
    print("✅ oauth2client: 설치됨 (deprecated)")
except ImportError:
    print("⚠️ oauth2client 미설치 (google-auth 사용 권장)")

print("\n" + "=" * 70)
print("진단 완료")
print("=" * 70)
