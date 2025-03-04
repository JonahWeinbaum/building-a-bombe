import numpy as np
import matplotlib.pyplot as plt

# Sample data: Replace with your own True/False values
data = np.array([[True, False, True],
                 [False, True, False],
                 [True, True, False]])

# Convert boolean to integer for visualization
data_int = data.astype(int)

# Create a heatmap
plt.imshow(data_int, cmap='RdYlGn', interpolation='nearest')
plt.xticks(ticks=[0, 1, 2], labels=['Column 1', 'Column 2', 'Column 3'])
plt.yticks(ticks=[0, 1, 2], labels=['Row 1', 'Row 2', 'Row 3'])
plt.title('Boolean Value Visualization')
plt.show()
