import random
import streamlit as st

# Define the groups and words with colors
GROUPS = {
    "Best": (["Selling", "Kown", "Ever", "Fit"], "#D8BFD8"),  # Light Yellow
    "Newbie": (["Rookie", "Starter", "Novice", "A Baby"], "#98FB98"),  # Light Green
    "Gym": (["Gossip", "Lifestyle", "Be strong", "Good time"], "#ADD8E6"),  # Light Blue
    "Buddy": (["Friend", "Partner", "Pal", "Teammate"], "#FFFACD"),  # Light Purple
}

# Initialize words and shuffle only once
if "WORDS" not in st.session_state:
    st.session_state.WORDS = [(word, group, color) for group, (words, color) in GROUPS.items() for word in words]
    random.shuffle(st.session_state.WORDS)

# Initialize state for selected words and correct groups
if "selected_words" not in st.session_state:
    st.session_state.selected_words = []
if "correct_groups" not in st.session_state:
    st.session_state.correct_groups = []

# Helper function to lighten a HEX color
def lighten_color(hex_color, amount=0.5):
    """Lighten the given HEX color by the specified amount (0-1)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return f"#{r:02x}{g:02x}{b:02x}"

# Check selected words for correctness
def check_group():
    selected_words = st.session_state.selected_words
    if len(selected_words) != 4:
        st.warning("You must select exactly 4 words!")
        return

    # Determine the groups of selected words
    groups = set(word[1] for word in st.session_state.WORDS if word[0] in selected_words)
    if len(groups) == 1:  # All words belong to the same group
        group = groups.pop()
        if group in st.session_state.correct_groups:
            st.warning(f"You already found the '{group}' group.")
        else:
            st.session_state.correct_groups.append(group)
            st.success(f"Correct! You've completed the '{group}' group.")
            # Remove completed group words from the word list
            st.session_state.WORDS = [
                (word, g, color) for word, g, color in st.session_state.WORDS if g != group
            ]
    else:
        st.error("Incorrect group! Try again.")

    # Reset the selected words
    st.session_state.selected_words = []

# Render word buttons
cols = st.columns(4)
for i, (word, group, color) in enumerate(st.session_state.WORDS):
    with cols[i % 4]:
        # Determine button appearance based on selection
        button_color = lighten_color(color) if word in st.session_state.selected_words else color
        button_style = f"background-color: {button_color}; color: black; padding: 10px; border-radius: 5px; border: none;"

        if st.button(
            word,
            key=f"word_{word}",
            help=f"Group: {group}",
            args=(word,),
            use_container_width=True,
        ):
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
