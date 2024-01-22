from src.parse_md import parse_markdown

def test_parsing():
    # Test parsing with the example file
    with open('assets/example.md', 'r') as file:
        example_md_content = file.read()
    parsed_data = parse_markdown(example_md_content)

    for chapter in parsed_data:
        print(f"Chapter: {chapter.title}")
        print("Questions:")
        for question in chapter.questions:
            print(f"  - {question.text}")
            if question.options:
                print("    Options:")
                for option in question.options:
                    print(f"      {option[0]} {option[1]}")
            print(f"    Correct Answer: {question.correct_answer}")
            print()
