from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import pandas as pd
import time


# Visualization functions
def lifespan_bar_chart(dog_data, order, number):
    sorted_data = dog_data.sort_values('Avg Lifespan (Yrs)', ascending=order).head(number)
    dog_breeds = sorted_data['Breed']
    lifespans = sorted_data['Avg Lifespan (Yrs)']

    plt.figure(figsize=(10, 6))
    plt.bar(dog_breeds, lifespans, color='skyblue')
    plt.ylabel('Lifespan (Years)')
    plt.xlabel('Dog Breed')
    if not order:
        plt.title(f'Top {number} Longest-Lived Dog Breeds')
    else:
        plt.title(f'Top {number} Shortest-Lived Dog Breeds')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def weight_histogram(dog_data):
    plt.figure(figsize=(8, 5))
    plt.hist(dog_data['Avg Weight (lbs)'].dropna(), bins=10, color='green', edgecolor='black')
    average_weight = dog_data['Avg Weight (lbs)'].mean()
    plt.axvline(average_weight, color='red', linestyle='dashed', linewidth=2, label=f'Average Weight: {average_weight:.2f} lbs')
    plt.xlabel('Weight (lbs)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Dog Weights')
    plt.legend()
    plt.show()


def weight_vs_lifespan_scatter(dog_data):
    weights = dog_data['Avg Weight (lbs)']
    lifespans = dog_data['Avg Lifespan (Yrs)']
    breeds = dog_data['Breed']

    # Create a DataFrame for Plotly
    scatter_data = pd.DataFrame({
        'Weight (lbs)': weights,
        'Lifespan (Years)': lifespans,
        'Breed': breeds
    })

    # Create the scatter plot
    fig = px.scatter(
        scatter_data,
        x='Weight (lbs)',
        y='Lifespan (Years)',
        hover_name='Breed',  # This will show the breed name on hover
        title="Weight vs Lifespan of Dog Breeds"
    )

    # Update layout for better appearance
    fig.update_traces(marker=dict(size=10, color='orange', opacity=0.7))
    fig.update_layout(
        xaxis_title="Weight (lbs)",
        yaxis_title="Lifespan (Years)"
    )

    # Show the interactive plot
    fig.show()


def trainability_boxplot(dog_data):
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Trainable', y='Avg Lifespan (Yrs)', data=dog_data)
    plt.title('Lifespan Distribution by Trainability')
    plt.show()


def shedding_bar_chart(dog_data, num_breeds):
    top_shedding = dog_data.sort_values('Shedding', ascending=False).head(num_breeds)
    least_shedding = dog_data.sort_values('Shedding', ascending=True).head(num_breeds)
    top_and_least_shedding = pd.concat([top_shedding, least_shedding])

    plt.figure(figsize=(10, 6))
    plt.bar(top_and_least_shedding['Breed'], top_and_least_shedding['Shedding'])
    plt.xlabel('Dog Breed')
    plt.ylabel('Shedding Level')
    plt.title(f'Top and Least {num_breeds} Shedding Dog Breeds')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def shedding_wordcloud(dog_data):
    high_shedding_breeds = dog_data[dog_data['Shedding'] >= 4]['Breed']
    text = ' '.join(high_shedding_breeds)
    wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=set(STOPWORDS), min_font_size=10).generate(text)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


# Main menu
def main(dog_data):
    while True:
        print("\nDog Breed Visualizations Menu")
        print("1. Lifespan Bar Chart (Longest/Shortest-Lived Breeds)")
        print("2. Weight Distribution Histogram")
        print("3. Weight vs Lifespan Scatter Plot")
        print("4. Lifespan Distribution by Trainability Box Plot")
        print("5. Top/Least Shedding Breeds Bar Chart")
        print("6. High-Shedding Dog Breeds Word Cloud")
        # print("7. Browse Dog Breeds")
        print("7. Exit")

        choice = input("Choose an option (1-7): ")

        if choice == '1':
            order = bool(int(input("Do you want to see the breeds with the longest lifespan or shortest? Enter 0 for long and 1 for short: ")))
            number = int(input("How many breeds would you like to see? "))
            lifespan_bar_chart(dog_data, order, number)
        elif choice == '2':
            weight_histogram(dog_data)
        elif choice == '3':
            weight_vs_lifespan_scatter(dog_data)
        elif choice == '4':
            trainability_boxplot(dog_data)
        elif choice == '5':
            num_breeds = int(input("Enter the number of top/least shedding breeds you'd like to see: "))
            shedding_bar_chart(dog_data, num_breeds)
        elif choice == '6':
            shedding_wordcloud(dog_data)
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")
        time.sleep(2)
