import plotly.graph_objects as go

class MetricsVisualizer:
    def __init__(self, metrics):
        self.metrics = metrics
        self.figures = []  # List to store figure objects


    def plot_gender_definition_words(self):
        labels = ['Female', 'Male', 'Non-Binary', 'Trans', 'Cis']
        values = [
            self.metrics['percentage_of_female_gender_definition_words'],
            self.metrics['percentage_of_male_gender_definition_words'],
            self.metrics['percentage_of_non_binary_gender_definition_words'],
            self.metrics['percentage_of_trans_gender_definition_words'],
            self.metrics['percentage_of_cis_gender_definition_words']
        ]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Percentage of Gender Definition Words')
        self.figures.append(fig) 
        fig.show()

    def plot_bias_ratios(self):
        metrics = {
            'avg_bias_ratio': 'Average Bias Ratio',
            'avg_bias_conditional': 'Average Bias Conditional',
            'avg_bias_ratio_absolute': 'Average Bias Ratio Absolute',
            'avg_bias_conditional_absolute': 'Average Bias Conditional Absolute',
            'avg_non_binary_bias_ratio': 'Average Non-Binary Bias Ratio',
            'avg_non_binary_bias_conditional': 'Average Non-Binary Bias Conditional',
            'avg_non_binary_bias_ratio_absolute': 'Average Non-Binary Bias Ratio Absolute',
            'avg_non_binary_bias_conditional_absolute': 'Average Non-Binary Bias Conditional Absolute',
        }

        fig = go.Figure()
        for metric_key, metric_name in metrics.items():
            fig.add_trace(go.Bar(y=[metric_name], x=[self.metrics['additional_metrics'][metric_key]], orientation='h', name=metric_name))

        fig.update_layout(title='Metrics', yaxis=dict(title='Metrics'), showlegend=False)
        self.figures.append(fig) 
        fig.show()

    def plot_gender_distribution_in_tokens(self):
        tokens = list(self.metrics['token_based_metrics'].keys())
        genders = ['female_count', 'male_count', 'non_binary_count', 'trans_count', 'cis_count']
        traces = []
        for gender in genders:
            trace = go.Bar(
                x=tokens,
                y=[self.metrics['token_based_metrics'][token][gender] for token in tokens],
                name=gender.split('_')[0].capitalize()  # Extracting gender name from key
            )
            traces.append(trace)

        layout = go.Layout(
            title='Gender Distribution in Token Definitions',
            xaxis=dict(title='Tokens'),
            yaxis=dict(title='Count'),
            barmode='stack'
        )
        fig = go.Figure(data=traces, layout=layout)
        self.figures.append(fig) 
        fig.show()

    def plot_bias_ratio_for_each_token(self):
        tokens = list(self.metrics['token_based_metrics'].keys())
        token_names = [token.capitalize() for token in tokens]
        fig = go.Figure()
        for ratio in ['bias_ratio']:
            fig.add_trace(go.Bar(
                x=token_names,
                y=[self.metrics['token_based_metrics'][token][ratio] for token in tokens],
            ))
        fig.update_layout(title='Bias Ratio for Each Token',
                          xaxis_title='Tokens',
                          yaxis_title='Bias Ratio')
        self.figures.append(fig) 
        fig.show()

    def plot_statistics(self):
        statistics = {
            'freq Cutoff': self.metrics['statistics']['frequency_cutoff'],
            'No of Words Considered': self.metrics['statistics']['num_words_considered'],
            'freq of Female Gender Definition Words': self.metrics['statistics']['freq_of_female_gender_definition_words'],
            'freq of Male Gender Definition Words': self.metrics['statistics']['freq_of_male_gender_definition_words'],
            'freq of Non-Binary Gender Definition Words': self.metrics['statistics']['freq_of_non_binary_gender_definition_words'],
            'Jensen-Shannon Divergence': self.metrics['statistics']['jsd'],
        }

        fig = go.Figure()
        fig.add_trace(go.Bar(y=list(statistics.keys()), x=list(statistics.values()), orientation='h'))
        fig.update_layout(title='Statistics')
        self.figures.append(fig) 
        fig.show()
    
    def save_plots_to_html(self, file_name='all_plots.html'):
        # Save all figures in the self.figures list to a single HTML file
        with open(file_name, 'w') as f:
            for fig in self.figures:
                f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
                f.write('<hr>')  # Add a horizontal line between plots for better separation
# Example usage:
# metrics_all = ...  # Your metrics data here
# visualizer = MetricsVisualizer(metrics_all)
# visualizer.plot_gender_definition_words()
# visualizer.plot_bias_ratios()
# ...
import plotly.express as px
import plotly.graph_objects as go

class DataFrameVisualizer:
    def __init__(self, dataframe):
        self.df = dataframe

    def plot_line(self, x, y, title="Line Plot"):
        """Generate a line plot."""
        fig = px.line(self.df, x=x, y=y, title=title)
        fig.show()
        return fig

    def plot_bar(self, x, y, title="Bar Chart"):
        """Generate a bar chart."""
        fig = px.bar(self.df, x=x, y=y, title=title)
        fig.show()
        return fig

    def plot_pie(self, names, values, title="Pie Chart"):
        """Generate a pie chart."""
        fig = px.pie(self.df, names=names, values=values, title=title)
        fig.show()
        return fig

    def plot_histogram(self, x, title="Histogram"):
        """Generate a histogram."""
        fig = px.histogram(self.df, x=x, title=title)
        fig.show()
        return fig

    def plot_scatter(self, x, y, color="year", title="Scatter Plot"):
        """Generate a scatter plot."""
        fig = px.scatter(self.df, x=x, y=y, color=color, title=title)
        fig.show()
        return fig

    def plot_heatmap(self, x, y, z, title="Heatmap"):
        """Generate a heatmap."""
        fig = go.Figure(data=go.Heatmap(
            z=self.df[z],
            x=self.df[x],
            y=self.df[y],
            colorscale='Viridis'))
        fig.update_layout(title=title)
        fig.show()
        return fig

    # Add more plot types as needed
