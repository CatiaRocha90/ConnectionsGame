import streamlit as st
import random

# Define the groups and words with colors
GROUPS = {
    "Best": (["Selling", "Known", "Ever", "Fit"], "#D8BFD8"),  # Light Yellow
    "Newbie": (["Rookie", "Starter", "Novice", "A Baby"], "#98FB98"),  # Light Green
    "Gym": (["Gossip", "Lifestyle", "Be strong", "Good time"], "#ADD8E6"),  # Light Blue
    "Buddy": (["Friend", "Partner", "Pal", "Teammate"], "#FFFACD"),  # Light Purple
}

# Create a shuffled list of words
WORDS = [(word, group, color) for group, (words, color) in GROUPS.items() for word in words]
random.shuffle(WORDS)

# Initialize Streamlit session state
if "selected_words" not in st.session_state:
    st.session_state.selected_words = []
if "correct_groups" not in st.session_state:
    st.session_state.correct_groups = []
if "game_completed" not in st.session_state:
    st.session_state.game_completed = False

def check_group():
    """Checks if the selected words form a valid group."""
    selected_words = st.session_state.selected_words
    if len(selected_words) != 4:
        st.warning("You must select exactly 4 words!")
        return

    # Check if the selected words belong to the same group
    groups = {group for word, group, color in WORDS if word in selected_words}
    if len(groups) == 1:
        group = groups.pop()
        if group in st.session_state.correct_groups:
            st.warning(f"You already found the '{group}' group!")
        else:
            st.session_state.correct_groups.append(group)
            st.success(f"Correct! You found the '{group}' group.")
            # Disable all words in the found group
            for i, (word, g, color) in enumerate(WORDS):
                if g == group:
                    WORDS[i] = (word, g, "white")  # Set the button to appear "disabled"

            # Check if the game is complete
            if len(st.session_state.correct_groups) == len(GROUPS):
                st.session_state.game_completed = True
    else:
        st.error("Incorrect! The selected words don't belong to the same group.")

    # Reset selected words
    st.session_state.selected_words = []

def display_game_board():
    """Displays the game board with interactive buttons."""
    st.write("Select 4 words that belong to the same group. Find all 4 groups to win!")
    cols = st.columns(4)
    for i, (word, group, color) in enumerate(WORDS):
        disabled = (
            group in st.session_state.correct_groups or
            st.session_state.game_completed
        )
        # Display the word as a button
        with cols[i % 4]:
            if st.button(
                word,
                key=f"word_{i}",
                disabled=disabled,
                help="Click to select this word",
                use_container_width=True,
            ):
                # Handle word selection
                if word not in st.session_state.selected_words:
                    st.session_state.selected_words.append(word)

    # Display selected words
    if st.session_state.selected_words:
        st.write(f"### Selected: {', '.join(st.session_state.selected_words)}")

# Main App Logic
st.title("Connections Game")
if not st.session_state.game_completed:
    display_game_board()

    # Button to check group validity
    if st.button("Check Group"):
        check_group()
else:
    st.balloons()
    st.write("### Congratulations! You completed the game.")
    st.write("Here are the groups in order:")

    group_order = ["Best", "Newbie", "Gym", "Buddy"]
    for group in group_order:
        words = [word for word, g, color in WORDS if g == group]
        color = GROUPS[group][1]
        st.markdown(f"#### <span style='color:{color}'>{group}</span>", unsafe_allow_html=True)
        st.write(", ".join(words))
