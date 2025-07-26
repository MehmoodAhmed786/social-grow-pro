import time
import random
from playwright.sync_api import Playwright, sync_playwright, expect
import streamlit as st

def run(playwright: Playwright, username: str, password: str, post_links: list, explore_limit: int, accounts_to_follow: list, comments: list) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

  
    page.goto("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")
    time.sleep(10)

   
    try:
        page.get_by_role("button", name="Not now").click()
    except Exception:
        print("No 'Not Now' button found.")
    time.sleep(2)

    
    for post_link in post_links:
        page.goto(post_link)
        time.sleep(5)

        
        page.locator(".x1lliihq > div > div").first.dblclick()
        print(f"Post {post_link} liked successfully!")
        time.sleep(5)

      
        comment_box = page.get_by_placeholder("Add a comment…")
        comment = random.choice(comments)
        comment_box.click()
        comment_box.fill(comment)
        time.sleep(1)
        page.get_by_role("button", name="Post").click()

        print(f"Commented on post: {post_link} with '{comment}'")
        time.sleep(5)

    
    page.goto("https://www.instagram.com/explore/")
    time.sleep(5)

    for _ in range(explore_limit):
        try:
            first_post = page.get_by_role("main").first
            first_post.click()
            time.sleep(5)
            page.get_by_role("button", name="Next").click()
            time.sleep(10)
            page.get_by_role("button", name="Next").click()
            print("Closed the post.")
            time.sleep(3)

        except Exception as e:
            print(f"An error occurred while exploring: {e}")
            break

    
    for account_link in accounts_to_follow:
        page.goto(account_link)
        time.sleep(5)
        try:
            page.click("button:has-text('Follow')")
            print(f"Followed account: {account_link}")
            time.sleep(random.randint(2, 5))
        except Exception as e:
            print(f"An error occurred while following {account_link}: {e}")

    context.close()
    browser.close()

def main():
    st.title("Instagram Bot")
    st.write("Automate liking and commenting on Instagram posts, exploring, and following accounts.")

    num_accounts = st.number_input("How many accounts do you want to use?", min_value=1, max_value=10)
    accounts = []
    
    for i in range(num_accounts):
        username = st.text_input(f"Username for Account {i + 1}", key=f"username_{i}")
        password = st.text_input(f"Password for Account {i + 1}", type="password", key=f"password_{i}")
        accounts.append((username, password))

    num_posts = st.number_input("How many posts do you want to like and comment on?", min_value=1, max_value=10)
    post_links = []
    
    for i in range(num_posts):
        post_link = st.text_input(f"Post Link {i + 1}", key=f"post_link_{i}")
        post_links.append(post_link)

    explore_limit = st.number_input("How many posts to interact with from Explore?", min_value=1, max_value=20)

    num_accounts_to_follow = st.number_input("How many accounts do you want to follow?", min_value=1, max_value=10)
    accounts_to_follow = []
    
    for i in range(num_accounts_to_follow):
        account_link = st.text_input(f"Account Link to Follow {i + 1}", key=f"follow_link_{i}")
        accounts_to_follow.append(account_link)

    
    num_comments = st.number_input("How many comments do you want to add?", min_value=1, max_value=10)
    comments = []
    
    for i in range(num_comments):
        comment = st.text_input(f"Comment {i + 1}", key=f"comment_{i}")
        comments.append(comment)

    if st.button("Run Bot"):
        if (all(username for username, _ in accounts) and
                all(password for _, password in accounts) and
                all(post_links) and
                explore_limit > 0 and
                all(accounts_to_follow) and
                all(comments)):
            for username, password in accounts:
                with sync_playwright() as playwright:
                    run(playwright, username, password, post_links, explore_limit, accounts_to_follow, comments)
            st.success("Successfully liked, commented, explored, and followed accounts for all accounts!")
        else:
            st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()
