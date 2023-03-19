import os
import openai

from typing import Any, Dict, List


def main(args: Any) -> None:
    """
    Main method.

    Parameters
    ----------
    args : Any
        Command line arguments.
    """
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "あなたは日本語でコミュニケーションできる有能なアシスタントです。"}
    ]
    
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # 最初の返答は読み捨てる
    # 例) ありがとうございます。私は常に最善を尽くして、お客様のニーズに応えるよう努めます。
    #     何かお手伝いできることがあれば、お気軽にお申し付けください。
    _ = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    try:
        while True:
            request = input("You: ")
            messages.append({"role": "user", "content": request})

            if len(messages) > 10:
                messages.pop(0)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            if response is not None:
                finish_reason = response["choices"][0]["finish_reason"]
                if finish_reason == "stop":
                    answer = response["choices"][0]["message"]["content"]
                    messages.append({"role": "assistant", "content": answer})
                    print(f"Assistant: {answer}")

                else:
                    print(f"error: Invalid finish reason: {finish_reason}.")
                    break
            else:
                print("error: response is null.")
                break

    except KeyboardInterrupt:
        pass

    except Exception as err:
        print(err)


if __name__ == '__main__':
    main(None)
