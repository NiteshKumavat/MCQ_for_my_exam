import streamlit as st
import json

def main():
    st.set_page_config(page_title="MCQ Quiz", page_icon="📝", layout="wide")
    st.title("🎓 MCQ Practice Test")
    st.subheader("Detailed Review Mode")
    st.divider()

    # Load JSON
    with open("MCQ.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract chapter
    chapters = list(data.keys())
    chapter_name = st.selectbox("📘 Select Chapter", chapters)
    question_bank = data[chapter_name]


    st.write(f"### 📘 Chapter: {chapter_name}")

    # Store user answers
    user_answers = {}

    # 1. Display Questions
    for q_id, q_data in question_bank.items():
        st.write(f"### Question {q_id}")
        st.write(q_data["question"])

        if chapter_name == "Chp 5 Part II" and q_id == "37" :
            st.image("./images/img.png")

        choice = st.radio(
            "Select your answer:",
            options=q_data["options"],
            index=None,
            key=f"q_{q_id}"
        )

        user_answers[q_id] = choice
        st.write("---")

    # 2. Submit Button
    if st.button("Submit Test & View Results", type="primary"):
        score = 0
        detailed_results = []

        for q_id, q_data in question_bank.items():
            user_choice = user_answers[q_id]
            correct_letter = q_data["answer"].lower()

            # Get correct option text
            correct_option_text = next(
                (opt for opt in q_data["options"] if opt.lower().startswith(f"({correct_letter})") or opt.lower().startswith(f"{correct_letter})")),
                "N/A"
            )

            if user_choice:
                user_letter = user_choice.split(")")[0].replace("(", "").lower()

                if user_letter == correct_letter:
                    score += 1
                    status = "correct"
                else:
                    status = "wrong"

                detailed_results.append({
                    "id": q_id,
                    "status": status,
                    "text": q_data["question"],
                    "user": user_choice,
                    "correct": correct_option_text
                })
            else:
                detailed_results.append({
                    "id": q_id,
                    "status": "unattempted",
                    "text": q_data["question"],
                    "user": "Not Attempted",
                    "correct": correct_option_text
                })

        # 3. Show Score
        st.header(f"🎯 Final Score: {score} / {len(question_bank)}")
        st.progress(score / len(question_bank))

        # 4. Detailed Review
        st.header("📊 Detailed Review")

        for res in detailed_results:
            icon = "✅" if res["status"] == "correct" else "❌"

            with st.expander(f"Question {res['id']}: {icon}"):
                st.write(f"**Question:** {res['text']}")

                if res["status"] == "correct":
                    st.success(f"**Your Answer:** {res['user']}")
                elif res["status"] == "wrong":
                    st.error(f"**Your Answer:** {res['user']}")
                    st.info(f"**Correct Answer:** {res['correct']}")
                else:
                    st.warning("**Not Attempted**")
                    st.info(f"**Correct Answer:** {res['correct']}")

if __name__ == "__main__":
    main()