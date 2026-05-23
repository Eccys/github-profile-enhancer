#!/usr/bin/env python3
import json
import os
import sys

def load_data():
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data.json: {e}")
        sys.exit(1)

def select_items(category_name, items):
    print(f"\nSelect your {category_name} (enter numbers separated by commas, e.g., 1,3,5):")
    for idx, item in enumerate(items, 1):
        print(f"[{idx}] {item['name']}")
    
    choices = input("Your selection: ").strip()
    selected = []
    if not choices:
        return selected
    
    try:
        indices = [int(i.strip()) for i in choices.split(",") if i.strip()]
        for idx in indices:
            if 1 <= idx <= len(items):
                selected.append(items[idx-1])
    except ValueError:
        print("[!] Invalid input. Skipping selection for this category.")
        
    return selected

def main():
    print("=" * 60)
    print("      🌟 Welcome to the GitHub Profile README Generator 🌟      ")
    print("=" * 60)
    print("This tool will guide you to create a premium, high-converting")
    print("GitHub Profile README complete with stats, badges, and donation links.")
    print("-" * 60)

    # Basic Info
    name = input("Enter your full name or display name: ").strip() or "Developer"
    tagline = input("Enter a catchy tagline/description (e.g., Full Stack Engineer building SaaS): ").strip() or "A passionate developer building awesome things."
    github_user = input("Enter your GitHub username: ").strip()
    if not github_user:
        print("[!] GitHub username is required to generate stats widgets.")
        sys.exit(1)

    # Load badges
    data = load_data()

    # Selections
    selected_languages = select_items("Languages", data["languages"])
    selected_frameworks = select_items("Frameworks & Libraries", data["frameworks"])
    selected_tools = select_items("Tools & DevOps", data["tools"])
    selected_databases = select_items("Databases", data["databases"])
    selected_socials = select_items("Social Links", data["socials"])

    # Collect social URLs
    socials_markdown = []
    for item in selected_socials:
        url = input(f"Enter your link/username for {item['name']}: ").strip()
        if url:
            # If they just entered a username, help format it for common sites
            if not url.startswith("http"):
                if item["name"].lower() == "linkedin":
                    url = f"https://linkedin.com/in/{url}"
                elif item["name"].lower() == "twitter/x":
                    url = f"https://x.com/{url}"
                elif item["name"].lower() == "discord":
                    url = f"https://discord.com/users/{url}"
                elif item["name"].lower() == "youtube":
                    url = f"https://youtube.com/@{url}"
                elif item["name"].lower() == "instagram":
                    url = f"https://instagram.com/{url}"
                elif item["name"].lower() == "medium":
                    url = f"https://medium.com/@{url}"
                elif item["name"].lower() == "dev.to":
                    url = f"https://dev.to/{url}"
                elif item["name"].lower() == "github":
                    url = f"https://github.com/{url}"
            socials_markdown.append(f'<a href="{url}" target="_blank"><img src="{item["badge"]}" /></a>')

    # Monetization Links
    print("\n" + "-" * 50)
    print("💰 Monetization Setup (Support & Sponsorships)")
    print("Leave empty if you wish to skip a donation link.")
    print("-" * 50)
    kofi = input("Enter Ko-fi username (optional): ").strip()
    buymeacoffee = input("Enter Buy Me a Coffee username (optional): ").strip()
    paypal = input("Enter PayPal username/link (optional): ").strip()

    # Compile the Markdown content
    readme_content = []
    
    # 1. Header
    readme_content.append(f"""# Hey there! I'm {name} 👋
    
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=61DAFB&center=true&vCenter=true&width=435&lines={tagline.replace(' ', '+')}" alt="Typing SVG" />
</p>
""")

    # 2. About Me / Tagline
    readme_content.append(f"""
## 🚀 About Me
I am a builder, open-source enthusiast, and creator. Feel free to explore my repositories, star my projects if you find them helpful, or get in touch!

- 💻 I’m currently working on open-source packages and applications.
- ⚡ Fun fact: I love automating workflows to save developer hours.
""")

    # 3. Socials
    if socials_markdown:
        readme_content.append("## 🌐 Connect with Me\n<p align=\"left\">\n" + "\n".join([f"  {link}" for link in socials_markdown]) + "\n</p>\n")

    # 4. Tech Stack Badges
    readme_content.append("## 🛠️ Tech Stack & Skills\n")
    
    def format_badges(category_name, selected):
        lines = []
        if selected:
            lines.append(f"### {category_name}")
            badges_line = " ".join([f'<img src="{item["badge"]}" alt="{item["name"]}" />' for item in selected])
            lines.append(f"<p align=\"left\">\n  {badges_line}\n</p>\n")
        return "\n".join(lines)

    readme_content.append(format_badges("Programming Languages", selected_languages))
    readme_content.append(format_badges("Frameworks & Libraries", selected_frameworks))
    readme_content.append(format_badges("Tools & DevOps", selected_tools))
    readme_content.append(format_badges("Databases & Cloud", selected_databases))

    # 5. Stats Cards (Dynamic Widgets)
    readme_content.append(f"""
## 📊 GitHub Analytics

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username={github_user}&show_icons=true&theme=tokyonight&count_private=true" alt="GitHub Stats" width="48%" />
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username={github_user}&layout=compact&theme=tokyonight&count_private=true" alt="Top Languages" width="48%" />
</p>

<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user={github_user}&theme=tokyonight" alt="GitHub Streak" width="97%" />
</p>
""")

    # 6. Monetization Template
    has_donation = kofi or buymeacoffee or paypal
    if has_donation:
        readme_content.append("## 💖 Support My Work\n")
        readme_content.append("If you find my tools, templates, or open-source work helpful, consider buying me a coffee! Your support helps me keep building and maintaining open-source software.\n")
        readme_content.append("<p align=\"left\">")
        if kofi:
            readme_content.append(f'  <a href="https://ko-fi.com/{kofi}" target="_blank"><img src="https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-fi" /></a>')
        if buymeacoffee:
            readme_content.append(f'  <a href="https://www.buymeacoffee.com/{buymeacoffee}" target="_blank"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee" /></a>')
        if paypal:
            # Handle paypal link or username
            paypal_url = paypal if paypal.startswith("http") else f"https://paypal.me/{paypal}"
            readme_content.append(f'  <a href="{paypal_url}" target="_blank"><img src="https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white" alt="PayPal" /></a>')
        readme_content.append("</p>\n")

    # Save to a file
    output_path = os.path.join(os.path.dirname(__file__), "SAMPLE_README.md")
    try:
        with open(output_path, "w") as f:
            f.write("\n".join(readme_content))
        print("\n" + "=" * 60)
        print(f"[+] Success! Customized profile README generated successfully.")
        print(f"[+] File saved at: {output_path}")
        print("=" * 60)
    except Exception as e:
        print(f"[!] Failed to write SAMPLE_README.md: {e}")

if __name__ == "__main__":
    main()
