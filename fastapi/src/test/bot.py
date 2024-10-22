import httpx
import asyncio

# 서버의 URL 설정
url = "http://127.0.0.1:8000/Llama"

# 테스트할 봇 User-Agent 리스트
bot_user_agents = [
    "Googlebot", "Bingbot", "Slurp", "DuckDuckBot", "Baiduspider",
    "YandexBot", "Sogou", "Exabot", "facebot", "ia_archiver"
]

async def test_bot_access(bot_agent: str):
    headers = {
        "User-Agent": bot_agent  # 봇 User-Agent로 설정
    }

    async with httpx.AsyncClient() as client:
        try:
            # 봇 User-Agent로 서버에 요청 (비동기)
            response = await client.post(url, headers=headers, json={"input_data": "Test question"})

            # 400번대 에러가 반환되면 봇 차단이 정상적으로 이루어짐
            if response.status_code == 400:
                print(f"Bot '{bot_agent}' access blocked successfully. Status code: {response.status_code}")
            else:
                print(f"Bot '{bot_agent}' access not blocked. Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error occurred while testing bot '{bot_agent}': {str(e)}")


async def run_tests():
    tasks = []
    for bot_agent in bot_user_agents:
        tasks.append(test_bot_access(bot_agent))

    # 모든 봇 테스트 작업을 비동기로 실행
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run_tests())
