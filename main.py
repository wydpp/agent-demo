from travel_agent_service import invoke_agent

if __name__ == "__main__":
    while True:
        user_input = input("请输入旅行目的城市(输入 'exit' 退出):")
        if user_input.lower() == "exit":
            print("程序退出")
            break
        # 运行agent
        invoke_agent(user_input)
