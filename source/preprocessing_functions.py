from source.libs import *
import source.config as config

class CrimeLocalizer:
    def __init__(self, dataframe, latitude, longitude):
        self.dataframe = dataframe.copy()
        self.latitude = latitude
        self.longitude = longitude

    def filter_data(self, districts, categories, limit):
        df_filtered = self.dataframe.iloc[0:limit, :]
        df_filtered = df_filtered[df_filtered['PdDistrict'].isin(districts)]
        df_filtered = df_filtered[df_filtered['Category'].isin(categories)]
        return df_filtered

    def generate_map(self, df_filtered, map_filename="crime_map.html"):
        map_filepath = os.path.join("static", map_filename)
        
        crime_map = folium.Map(location=[self.latitude, self.longitude], zoom_start=12)
        incidents = plugins.MarkerCluster().add_to(crime_map)

        for lat, lng, label in zip(df_filtered.Y, df_filtered.X, df_filtered.Category):
            folium.Marker(location=[lat, lng], icon=None, popup=label).add_to(incidents)
        
        crime_map.save(map_filepath)
        return map_filepath

    def generate_charts(self, df_filtered, chart_filename="crime_chart.png"):
        chart_filepath = os.path.join("static", chart_filename)
        
        cat_unique = df_filtered['Category'].value_counts().reset_index()
        dist_unique = df_filtered['PdDistrict'].value_counts().reset_index()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 20))
        ax1.bar(cat_unique['index'], cat_unique['Category'])
        ax1.set_title('Amount of Criminal Cases Based on Category',fontsize=12)
        ax2.bar(dist_unique['index'], dist_unique['PdDistrict'])
        ax2.set_title('Amount of Criminal Cases in Selected Districts',fontsize=12)

        plt.savefig(chart_filepath)
        plt.close()
        return chart_filepath

