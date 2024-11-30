import streamlit as st
import random
import time
import numpy as np
import cv2
import io
from PIL import Image

# Game logic variables
paddle_width = 100
ball_radius = 20
game_width = 800
game_height = 600

# Create a game state container
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'ball_position' not in st.session_state:
    st.session_state.ball_position = [random.randint(100, 700), 0]
if 'paddle_position' not in st.session_state:
    st.session_state.paddle_position = 350

# Function to generate the game screen image
def generate_game_screen():
    # Create a blank white canvas for the game
    img = np.ones((game_height, game_width, 3), dtype=np.uint8) * 255

    # Draw the paddle (a rectangle)
    paddle_start = st.session_state.paddle_position
    paddle_end = paddle_start + paddle_width
    cv2.rectangle(img, (paddle_start, game_height - 50), (paddle_end, game_height - 30), (0, 0, 255), -1)

    # Draw the falling ball (a circle)
    ball_x, ball_y = st.session_state.ball_position
    cv2.circle(img, (ball_x, ball_y), ball_radius, (0, 255, 0), -1)

    # Convert the image to an image that can be displayed in Streamlit
    pil_img = Image.fromarray(img)
    return pil_img

# Function to move the ball
def move_ball():
    ball_x, ball_y = st.session_state.ball_position
    ball_y += 5  # Move the ball down
    if ball_y >= game_height - 50 and (ball_x > st.session_state.paddle_position and ball_x < st.session_state.paddle_position + paddle_width):
        st.session_state.score += 1
        st.session_state.ball_position = [random.randint(100, 700), 0]  # Reset ball position after catching it
    elif ball_y >= game_height:
        st.session_state.ball_position = [random.randint(100, 700), 0]  # Reset ball position if missed

    st.session_state.ball_position = [ball_x, ball_y]

# Function to update the paddle position
def move_paddle(direction):
    if direction == 'left' and st.session_state.paddle_position > 0:
        st.session_state.paddle_position -= 20
    elif direction == 'right' and st.session_state.paddle_position < game_width - paddle_width:
        st.session_state.paddle_position += 20

# Main game loop
def main():
    st.title("Catch the Falling Object!")

    # Display the current score
    st.text(f"Score: {st.session_state.score}")

    # Control the paddle with buttons
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        move_left = st.button("Move Left")
    with col3:
        move_right = st.button("Move Right")

    if move_left:
        move_paddle('left')
    if move_right:
        move_paddle('right')

    # Move the ball
    move_ball()

    # Update the game screen
    game_screen = generate_game_screen()
    st.image(game_screen, use_column_width=True)

    # Pause for a moment before updating the game state
    time.sleep(0.05)

    # Restart game button
    if st.button("Restart Game"):
        st.session_state.score = 0
        st.session_state.ball_position = [random.randint(100, 700), 0]
        st.session_state.paddle_position = 350

if __name__ == "__main__":
    main()
