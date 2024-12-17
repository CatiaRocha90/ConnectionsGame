import streamlit as st
import random

# Define the groups and words with colors
GROUPS = {
    "Best": (["Selling", "Known", "Ever", "Fit"], "#D8BFD8"),  # Light Yellow
    "Newbie": (["Rookie", "Starter", "Novice", "A Baby"], "#98FB98"),  # Light Green
    "Gym": (["Gossip", "Lifestyle", "Be strong", "Good time"], "#ADD8E6"),  # Light Blue
    "Buddy": (["Friend", "Partner", "Pal", "Teammate"], "#FFFACD"),  # Light Purple
}

WORDS = [(word, group, color) for group, (words, color) in GROUPS.items() for word in words]
random.shuffle(WORDS)

# Initialize session state
if "selected_words" not in st.session_state:
    st.session_state.selected_words = []
if "correct_groups" not in st.session_state:
    st.session_state.correct_groups = []
if "game_completed" not in st.session_state:
    st.session_state.game_completed = False

def check_group():
    """Check if the selected words form a valid group."""
    selected_words = st.session_state.selected_words
    if len(selected_words) != 4:
        st.warning("You must select exactly 4 words!")
        return

    # Determine the groups of the selected words
    groups = {group for word, group, color in WORDS if word in selected_words}

    if len(groups) == 1:  # All words belong to the same group
        group = groups.pop()
        if group in st.session_state.correct_groups:
            st.warning(f"You already found the '{group}' group!")
        else:
            st.session_state.correct_groups.append(group)
            st.success(f"Correct! You found the '{group}' group.")
            if len(st.session_state.correct_groups) == 4:
                st.session_state.game_completed = True
    else:
        st.error("Incorrect! The selected words don't belong to the same group.")

    # Reset the selection
    st.session_state.selected_words = []

# Streamlit UI
st.title("Connections Game")
st.write("Select 4 words that belong to the same group. Find all 4 groups to win!")

# Display words as buttons
cols = st.columns(4)
for i, (word, group, color) in enumerate(WORDS):
    disabled = (
        word in st.session_state.selected_words or
        st.session_state.game_completed or
        group in st.session_state.correct_groups
    )
    with cols[i % 4]:
        if st.button(word, key=f"word_{i}", disabled=disabled):
            if word not in st.session_state.selected_words:
                st.session_state.selected_words.append(word)

# Show selected words
if st.session_state.selected_words:
    st.write("Selected Words:", ", ".join(st.session_state.selected_words))

# Check group button
if st.button("Check Group"):
    check_group()

# Game completion
if st.session_state.game_completed:
    st.balloons()
    st.write("### Congratulations! You've found all the groups:")
    
    group_order = ["Best", "Newbie", "Gym", "Buddy"]  # Desired order
    for group in group_order:
        words = [word for word, g, color in WORDS if g == group]
        title_color = GROUPS[group][1]
        st.markdown(f"#### <span style='color:{title_color};font-weight:bold'>{group}</span>", unsafe_allow_html=True)
        st.write(", ".join(words))
