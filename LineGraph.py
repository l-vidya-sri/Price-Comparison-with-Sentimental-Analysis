import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file into a DataFrame
def generate(dates, services):
    plt.clf()
  
    for s in services:
        plt.plot(dates, services[s], marker='o', label=s)
    
    
    # Add labels and title
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.title('Price History')

    # Add legend
    plt.subplots_adjust(bottom=0.2)
    plt.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Show the plot
    #plt.grid(True)
    #plt.tight_layout()
    img='line.png'
    plt.savefig(img, dpi=(1000))
    from PIL import Image
    im = Image.open(r''+str(img)+'')
    im.show()
