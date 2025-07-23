import pandas as pd
from datetime import datetime

# Load Excel dataset
df = pd.read_excel("Final Cricket Dataset.xlsx")
df["Last Match Date"] = pd.to_datetime(df["Last Match Date"], errors='coerce')
player_names = df["Name"].str.lower().tolist()

# Helper: get closest matching player name
def get_player_name(query):
    for name in player_names:
        if name in query.lower():
            return name
    return None

# Check if player is a top scorer (top 5)
def is_top_scorer(player_name):
    top_players = df.sort_values(by='International Runs', ascending=False).head(5)
    return player_name.lower() in top_players["Name"].str.lower().values

# Main function
def ask_crickchat(question: str) -> str:
    question = question.lower()
    player_name = get_player_name(question)

    if player_name:
        row = df[df["Name"].str.lower() == player_name].iloc[0]

        if "age" in question:
            return f"{row['Name']} is {row['Age']} years old."

        if "date of birth" in question or "dob" in question or "born" in question:
            return f"{row['Name']} was born on {row['DOB']}."

        if "place" in question or "belong" in question or "from" in question:
            return f"{row['Name']} is from {row['Place']}."

        if "test run" in question:
            return f"{row['Name']} has scored {row['Test Runs']} runs in Test matches."
        if "odi run" in question:
            return f"{row['Name']} has scored {row['ODI Runs']} runs in ODIs."
        if "t20 run" in question:
            return f"{row['Name']} has scored {row['T20 Runs']} runs in T20 Internationals."
        if "international run" in question:
            return f"{row['Name']} has scored {row['International Runs']} international runs in total."

        if "best performance" in question or "maximum" in question or "highest score" in question:
            return f"{row['Name']}'s best performance was when they scored {row['Maximum Score']} runs."

        if "last match date" in question or "when did" in question and "last match" in question or "last played" in question:
            return f"{row['Name']}'s last match was on {row['Last Match Date'].strftime('%B %d, %Y')}."
        if "last match venue" in question or "where did" in question and "last match" in question:
            return f"{row['Name']} played their last match at {row['Last Match Venue']}."
        if "last match run" in question or "how many runs" in question:
            return f"In the last match, {row['Name']} scored {row['Runs in Last Match']} runs."

        if "info" in question or "tell me" in question or "profile" in question:
            return (
                f"Here's what I found about {row['Name']}:\n"
                f"- Age: {row['Age']}\n"
                f"- Born: {row['DOB']} in {row['Place']}\n"
                f"- Test Runs: {row['Test Runs']}\n"
                f"- ODI Runs: {row['ODI Runs']}\n"
                f"- T20 Runs: {row['T20 Runs']}\n"
                f"- International Runs: {row['International Runs']}\n"
                f"- Highest Score: {row['Maximum Score']}\n"
                f"- Last Match: {row['Last Match Date'].strftime('%B %d, %Y')} at {row['Last Match Venue']}, scoring {row['Runs in Last Match']} runs."
            )

        if "how good" in question or "is" in question and "top scorer" in question:
            if is_top_scorer(player_name):
                return f"Yes, {row['Name']} is among the top international run-scorers for Pakistan!"
            else:
                return f"{row['Name']} is a solid performer, but not currently in the top 5."

        return f"I'm not sure how to answer that about {row['Name']}."

    # Global questions
    if "youngest" in question:
        row = df.loc[df["Age"].idxmin()]
        return f"The youngest player is {row['Name']}, who is {row['Age']} years old."

    if "oldest" in question:
        row = df.loc[df["Age"].idxmax()]
        return f"The oldest player is {row['Name']}, aged {row['Age']}."

    if "most test runs" in question:
        row = df.loc[df["Test Runs"].idxmax()]
        return f"{row['Name']} has the highest Test runs: {row['Test Runs']}."

    if "least test runs" in question:
        row = df.loc[df["Test Runs"].idxmin()]
        return f"{row['Name']} has the least Test runs: {row['Test Runs']}."

    if "most odi runs" in question:
        row = df.loc[df["ODI Runs"].idxmax()]
        return f"{row['Name']} has the highest ODI runs: {row['ODI Runs']}."

    if "least odi runs" in question:
        row = df.loc[df["ODI Runs"].idxmin()]
        return f"{row['Name']} has the least ODI runs: {row['ODI Runs']}."

    if "most t20 runs" in question:
        row = df.loc[df["T20 Runs"].idxmax()]
        return f"{row['Name']} has the highest T20 runs: {row['T20 Runs']}."

    if "least t20 runs" in question:
        row = df.loc[df["T20 Runs"].idxmin()]
        return f"{row['Name']} has the least T20 runs: {row['T20 Runs']}."

    if "most international runs" in question or "top scorer" in question:
        row = df.loc[df["International Runs"].idxmax()]
        return f"{row['Name']} has the most international runs: {row['International Runs']}."

    if "least international runs" in question:
        row = df.loc[df["International Runs"].idxmin()]
        return f"{row['Name']} has the least international runs: {row['International Runs']}."

    if "most runs in last match" in question:
        row = df.loc[df["Runs in Last Match"].idxmax()]
        return f"{row['Name']} scored the most in the last match: {row['Runs in Last Match']} runs."

    if "not played for a long time" in question:
        df_sorted = df.sort_values(by="Last Match Date").head(3)
        return "\n".join([f"- {r['Name']} (last match: {r['Last Match Date'].strftime('%B %d, %Y')})" for _, r in df_sorted.iterrows()])

    if "last match recently" in question or "most recent match" in question:
        row = df.loc[df["Last Match Date"].idxmax()]
        return f"The most recent match was played by {row['Name']} on {row['Last Match Date'].strftime('%B %d, %Y')}."

    return "Sorry, I didn't quite get that. Try asking something else."
