import random
import streamlit as st

# Define word groups
groups = {
    "Best": ["Best", "Bestman", "Bestie", "Best-seller"],
    "Newbie": ["Newbie", "Newcomer", "Beginner", "Rookie"],
    "Gym": ["Gym", "Gymnast", "Gymnasium", "Gymwear"],
    "Buddy": ["Buddy", "Pal", "Companion", "Sidekick"]
}

# Define colors for the groups
group_colors = {
    "Best": "#FFD700",  # Gold
    "Newbie": "#ADD8E6",  # Light Blue
    "Gym": "#90EE90",  # Light Green
    "Buddy": "#DA70D6"  # Orchid
}

# Shuffle words
all_words = []
for group in groups.values():
    all_words.extend(group)
random.shuffle(all_words)

# State management
if "found_groups" not in st.session_state:
    st.session_state.found_groups = []
if "selected_words" not in st.session_state:
    st.session_state.selected_words = []

# Game title
st.title("Connections Game")

# Instructions
st.write(
    """
    Welcome to the Connections Game! 
    Select four words that belong to the same group. Once all four groups are correctly identified, the game will reveal the words organized by groups and color.
    """
)

# Display words as clickable buttons
columns = st.columns(4)
for i, word in enumerate(all_words):
    col = columns[i % 4]
    if word not in st.session_state.selected_words:
        if col.button(word):
            st.session_state.selected_words.append(word)

# Process selections
if len(st.session_state.selected_words) == 4:
    selected_group = None
    for group_name, group_words in groups.items():
        if set(st.session_state.selected_words) == set(group_words):
            selected_group = group_name
            break

    if selected_group:
        st.session_state.found_groups.append(selected_group)
        st.session_state.selected_words = []  # Reset selections
        st.success(f"Correct! You found the {selected_group} group.")
        all_words = [word for word in all_words if word not in groups[selected_group]]
    else:
        st.error("Those words don't form a valid group. Try again!")
        st.session_state.selected_words = []  # Reset selections

# Check if the game is complete
if len(st.session_state.found_groups) == 4:
    st.success("🎉 All groups have been found! 🎉")
    st.write("Here are the groups and their words:")

    for group_name in ["Best", "Newbie", "Gym", "Buddy"]:
        st.markdown(
            f"<h3 style='color:{group_colors[group_name]}'>{group_name}</h3>",
            unsafe_allow_html=True
        )
        st.write(", ".join(groups[group_name]))

    # Clear state for a new game
    if st.button("Play Again"):
        st.session_state.clear()

