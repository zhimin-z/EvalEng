"""
Generate PCA visualization of harness clusters.

This script:
1. Loads the curated cluster metadata from JSON
2. Loads the feature matrix from CSV
3. Performs PCA dimensionality reduction
4. Visualizes clusters with labeled points
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.decomposition import PCA
from adjustText import adjust_text
from matplotlib.patches import FancyArrowPatch

# Set seaborn style (no grid)
sns.set_theme(style="white")

# =============================================================================
# 1. LOAD DATA
# =============================================================================

# Load curated cluster metadata
clusters_file = Path(__file__).parent / '../data/rq1_cluster_curated.json'
with open(clusters_file) as f:
    cluster_data = json.load(f)

# Load feature matrix
feature_matrix_file = Path(__file__).parent / '../data/rq1_harness_feature_matrix.csv'
df_features = pd.read_csv(feature_matrix_file, index_col=0)

harnesses = list(df_features.index)
feature_matrix = df_features.values

print(f"Loaded {len(harnesses)} harnesses with {feature_matrix.shape[1]} features")
print(f"Loaded {len(cluster_data['clusters'])} curated clusters")

# =============================================================================
# 2. BUILD HARNESS-TO-CLUSTER MAPPING
# =============================================================================

# Create mapping from harness name to cluster info
harness_to_cluster_id = {}
harness_to_cluster_name = {}
cluster_id_to_name = {}

for cluster in cluster_data['clusters']:
    cluster_id = cluster['cluster_id']
    cluster_name = cluster['cluster_name']
    cluster_id_to_name[cluster_id] = cluster_name

    for member in cluster['members']:
        harness_to_cluster_id[member] = cluster_id
        harness_to_cluster_name[member] = cluster_name

# Get cluster labels in the same order as harnesses
cluster_labels = [harness_to_cluster_id.get(h, 0) for h in harnesses]
cluster_names = [harness_to_cluster_name.get(h, 'Unknown') for h in harnesses]

num_clusters = len(cluster_data['clusters'])

# =============================================================================
# 3. PCA PROJECTION
# =============================================================================

pca = PCA(n_components=2)
pca_result = pca.fit_transform(feature_matrix)

print(f"\nPCA explained variance: PC1={pca.explained_variance_ratio_[0]:.1%}, PC2={pca.explained_variance_ratio_[1]:.1%}")

# Create DataFrame for seaborn
pca_df = pd.DataFrame({
    'PC1': pca_result[:, 0],
    'PC2': pca_result[:, 1],
    'Harness': harnesses,
    'Cluster': cluster_names
})

# =============================================================================
# 4. VISUALIZATION
# =============================================================================

fig, ax = plt.subplots(figsize=(14, 11))

# Use seaborn scatterplot with hue for clusters
palette = sns.color_palette("tab10", num_clusters)
sns.scatterplot(
    data=pca_df,
    x='PC1', y='PC2',
    hue='Cluster',
    palette=palette,
    s=120,
    alpha=0.8,
    ax=ax,
    legend='full'
)

# Store original positions and create text annotations
texts = []
original_positions = []
for i, row in pca_df.iterrows():
    txt = ax.text(
        row['PC1'], row['PC2'],
        row['Harness'],
        fontsize=12,
        fontweight='bold',
        alpha=0.9
    )
    texts.append(txt)
    original_positions.append((row['PC1'], row['PC2']))

# Use adjustText WITHOUT arrowprops to avoid automatic arrows
if texts:
    adjust_text(
        texts,
        x=pca_df['PC1'].values,
        y=pca_df['PC2'].values,
        expand_points=(1.0, 1.0),
        expand_text=(1.0, 1.0),
        force_points=(1.0, 1.0),
        force_text=(0.5, 0.5),
        lim=50,
        ax=ax,
        only_move={'text': 'xy'},
    )

    # Manually add arrows ONLY for texts that moved significantly
    # Need to draw canvas first to get accurate bounding boxes
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    threshold = 0.2
    for i, txt in enumerate(texts):
        x_orig, y_orig = original_positions[i]

        # Get text bounding box in display coordinates, then convert to data coordinates
        bbox = txt.get_window_extent(renderer=renderer)
        bbox_data = bbox.transformed(ax.transData.inverted())

        # Get text center
        bbox_center_x = (bbox_data.x0 + bbox_data.x1) / 2
        bbox_center_y = (bbox_data.y0 + bbox_data.y1) / 2

        # Calculate distance from center to data point
        dx = x_orig - bbox_center_x
        dy = y_orig - bbox_center_y
        distance = np.sqrt(dx**2 + dy**2)

        # Arrow starts from center, offset to edge of bounding box in direction of data point
        if distance > 0:
            # Half-width and half-height of the bounding box (scaled down to reduce gap)
            half_width = (bbox_data.x1 - bbox_data.x0) / 2 * 0.8
            half_height = (bbox_data.y1 - bbox_data.y0) / 2 * 0.8

            # Normalize direction
            dir_x = dx / distance
            dir_y = dy / distance

            # Find intersection with bounding box edge
            # Scale factors to reach each edge
            if abs(dir_x) > 1e-6:
                t_x = half_width / abs(dir_x)
            else:
                t_x = float('inf')
            if abs(dir_y) > 1e-6:
                t_y = half_height / abs(dir_y)
            else:
                t_y = float('inf')

            # Use the smaller scale factor (first edge hit)
            t = min(t_x, t_y)

            arrow_start_x = bbox_center_x + dir_x * t
            arrow_start_y = bbox_center_y + dir_y * t
        else:
            arrow_start_x, arrow_start_y = bbox_center_x, bbox_center_y

        nearest_point = (arrow_start_x, arrow_start_y)

        if distance >= threshold:
            arrow = FancyArrowPatch(
                nearest_point, (x_orig, y_orig),
                arrowstyle='->',
                color='gray',
                lw=0.8,
                zorder=1,
                mutation_scale=15
            )
            ax.add_patch(arrow)

ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)', fontsize=14)
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)', fontsize=14)
ax.tick_params(axis='both', labelsize=12)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=2, fontsize=12, framealpha=1.0)
plt.tight_layout()

output_path = Path(__file__).parent / '../figures/rq1_pca.pdf'
plt.savefig(output_path, format='pdf', bbox_inches='tight')
print(f"Saved {output_path}")
