import streamlit as st
import random

# Define the groups and words with colors
GROUPS = {
    "Best": (["Selling", "Kown", "Ever", "Fit"], "#D8BFD8"),  # Light Yellow
    "Newbie": (["Rookie", "Starter", "Novice", "A Baby"], "#98FB98"),  # Light Green
    "Gym": (["Gossip", "Lifestyle", "Be strong", "Good time"], "#ADD8E6"),  # Light Blue
    "Buddy": (["Friend", "Partner", "Pal", "Teammate"], "#FFFACD"),  # Light Purple
}

# Flatten the groups into a single list of words
WORDS = [(word, group, color) for group, (words, color) in GROUPS.items() for word in words]

# Streamlit App
st.set_page_config(page_title="Connections Game", layout="centered")
st.title("Connections Game")
st.write("Select 4 words that belong to the same group.")

# State management
if "selected_words" not in st.session_state:
    st.session_state.selected_words = []
if "selected_word_states" not in st.session_state:
    st.session_state.selected_word_states = {word: False for word, _, _ in WORDS}
if "correct_groups" not in st.session_state:
    st.session_state.correct_groups = []
if "shuffled_words" not in st.session_state:
    st.session_state.shuffled_words = random.sample(WORDS, len(WORDS))

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
            st.warning("You already found this group.")
        else:
            st.session_state.correct_groups.append(group)
            st.success("Correct! You found a group.")
            # Disable the words in the completed group
            for word, g, _ in WORDS:
                if g == group:
                    st.session_state.selected_word_states[word] = None  # Mark as disabled
    else:
        st.error("Incorrect group! Try again.")

    # Reset the selected words
    for word in selected_words:
        if st.session_state.selected_word_states[word] is not None:
            st.session_state.selected_word_states[word] = False
    st.session_state.selected_words = []

# Render word buttons
cols = st.columns(4)
for i, (word, group, color) in enumerate(st.session_state.shuffled_words):
    with cols[i % 4]:
        if st.session_state.selected_word_states[word] is None:
            st.button(word, key=f"disabled_{word}", disabled=True, use_container_width=True)
        else:
            button_style = f"background-color: {color if st.session_state.selected_word_states[word] else '#FFFFFF'}; color: black;"
            if st.button(word, key=f"word_{word}", use_container_width=True, help=f"Group: {group}"):
                if st.session_state.selected_word_states[word]:
                    st.session_state.selected_words.remove(word)
                    st.session_state.selected_word_states[word] = False
                else:
                    st.session_state.selected_words.append(word)
                    st.session_state.selected_word_states[word] = True

# Display selected words
st.write(f"**Selected Words:** {', '.join(st.session_state.selected_words) if st.session_state.selected_words else 'None'}")

# Check Group Button
if st.button("Check Group"):
    check_group()

# Display correct groups
if st.session_state.correct_groups:
    st.write("### Correct Groups Found:")
    for _ in st.session_state.correct_groups:
        st.markdown(f"- **Group Found**")

# Check if game is completed
if len(st.session_state.correct_groups) == len(GROUPS):
    st.balloons()
    st.success("Congratulations! You found all groups!")
    st.write("### Final Groups:")
    for group, (words, color) in GROUPS.items():
        st.markdown(f"**{group}:** {', '.join(words)}")
    st.stop()
