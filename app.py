import random
import streamlit as st

# Define the groups and words with colors
GROUPS = {
    "Best": (["Selling", "Kown", "Ever", "Fit"], "#D8BFD8"),  # Light Yellow
    "Newbie": (["Rookie", "Starter", "Novice", "A Baby"], "#98FB98"),  # Light Green
    "Gym": (["Gossip", "Lifestyle", "Be strong", "Good time"], "#ADD8E6"),  # Light Blue
    "Buddy": (["Friend", "Partner", "Pal", "Teammate"], "#FFFACD"),  # Light Purple
}

# Flatten the groups into a single list of words and shuffle them
WORDS = [(word, group, color) for group, (words, color) in GROUPS.items() for word in words]
random.shuffle(WORDS)

# Streamlit App
st.set_page_config(page_title="Connections Game", layout="centered")
st.title("Connections Game")
st.write("Select 4 words that belong to the same group.")

# State management
if "selected_words" not in st.session_state:
    st.session_state.selected_words = []
if "correct_groups" not in st.session_state:
    st.session_state.correct_groups = []

# Helper function to check groups
def check_group():
    selected_words = st.session_state.selected_words
    if len(selected_words) != 4:
        st.warning("You must select exactly 4 words!")
        return

    # Check if all selected words belong to the same group
    groups = set(word[1] for word in WORDS if word[0] in selected_words)
    if len(groups) == 1:  # All words belong to the same group
        group = groups.pop()
        if group in st.session_state.correct_groups:
            st.warning(f"You already found the '{group}' group.")
        else:
            st.session_state.correct_groups.append(group)
            st.success(f"Correct! You've completed the '{group}' group.")
            # Disable the words in the completed group
            for word, g, _ in WORDS:
                if g == group:
                    WORDS.remove((word, g, _))
    else:
        st.error("Incorrect group! Try again.")

    # Reset the selected words
    st.session_state.selected_words = []

# Render word buttons
cols = st.columns(4)
for i, (word, group, color) in enumerate(WORDS):
    with cols[i % 4]:
        if st.button(word, key=f"word_{word}"):
            if word in st.session_state.selected_words:
                st.warning(f"'{word}' is already selected.")
            else:
                st.session_state.selected_words.append(word)

# Display selected words
st.write(f"**Selected Words:** {', '.join(st.session_state.selected_words) if st.session_state.selected_words else 'None'}")

# Check Group Button
if st.button("Check Group"):
    check_group()

# Display correct groups
if st.session_state.correct_groups:
    st.write("### Correct Groups Found:")
    for group in st.session_state.correct_groups:
        st.markdown(f"- **{group}**")

# Check if game is completed
if len(st.session_state.correct_groups) == len(GROUPS):
    st.balloons()
    st.success("Congratulations! You found all groups!")
    st.write("### Final Groups:")
    for group, (words, color) in GROUPS.items():
        st.markdown(f"**{group}:** {', '.join(words)}")
    st.stop()
