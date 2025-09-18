<h1>Hydrolytix – Agri Intelligence Dashboard</h1>

<h2>Description</h2>
The Hydrolytix Agri Intelligence Dashboard is a modular and interactive web-based application that provides deep insights into agricultural production data. It delivers advanced data visualization, forecasting, and trend analysis to support decision-making in the agricultural sector. Built using Python, Dash, and Plotly, the system is designed for scalability, user-friendliness, and extensibility.

<h2>Languages and Technologies Used</h2>
- <b>Python</b> (Core programming) <br/>
- <b>Dash (Flask-based)</b> (Web framework & UI) <br/>
- <b>Pandas</b> (Data processing and aggregation) <br/>
- <b>Plotly</b> (Interactive visualizations) <br/>
- <b>ReportLab</b> (Dynamic PDF report generation) <br/>
- <b>Custom CSS</b> (Styling with Grid and Flexbox)  

<h2>Environments Used</h2>
- <b>VS Code / PyCharm</b> (Development) <br/>
- <b>Web Browsers (Chrome, Firefox, Edge)</b> <br/>
- <b>Flask/Dash Server</b> (Local deployment) <br/>

<h2>Dashboard Walk-through:</h2>

<p align="center">
  <b>Overview Dashboard</b> <br/>
  <img src="https://i.postimg.cc/brwnnSqZ/image.png" style="max-height: 500px; width: auto;" alt="Overview Dashboard"/>
  <img src="https://i.postimg.cc/SR1MfQKD/image.png" style="max-height: 500px; width: auto;" alt="Overview Dashboard"/>
  <br /><br />

<p align="center">
  <b>Year Comparison Charts</b> <br/>
  <img src="https://i.postimg.cc/2j9bJ6zx/image.png" style="max-height: 500px; width: auto;" alt="Year Comparison"/>
  <img src="https://i.postimg.cc/KY545cqB/image.png" style="max-height: 500px; width: auto;" alt="Year Comparison"/>
  <br /><br />

<p align="center">
  <b>Forecasting Models</b> <br/>
  <img src="https://i.postimg.cc/Z54Wvyj4/image.png" style="max-height: 500px; width: auto;" alt="Forecasting"/>
  <img src="https://i.postimg.cc/rwjK1FYW/image.png" style="max-height: 500px; width: auto;" alt="Forecasting"/>
  <img src="https://i.postimg.cc/rpYsHZTw/image.png" style="max-height: 500px; width: auto;" alt="Forecasting"/>
  <br /><br />

<p align="center">
  <b>Trend Analysis</b> <br/>
  <img src="https://i.postimg.cc/tRzQCZ1h/image.png" style="max-height: 500px; width: auto;" alt="Trend Analysis"/>
  <img src="https://i.postimg.cc/dtWbrbj3/image.png" style="max-height: 500px; width: auto;" alt="Trend Analysis"/>
  <br /><br />

<p align="center">
  <b>Export & Reporting</b> <br/>
  <img src="https://i.postimg.cc/zBSMB6fJ/image.png" style="max-height: 500px; width: auto;" alt="Export and Reporting"/>
</p>

<h2>Key Features</h2>

- 📊 <b>Interactive Visualizations:</b> Donut charts, bar charts, line charts, and dual-axis plots  
- 🗂️ <b>Multi-tab Navigation:</b> Overview, Year Comparison, Forecasting, Trend Analysis, Export  
- 📅 <b>Filtering:</b> Filter data by season and year with real-time updates  
- 📈 <b>Forecasting Models:</b> ARIMA and Exponential Smoothing with evaluation metrics  
- 📄 <b>Reporting:</b> Export filtered data in CSV and professionally formatted PDF reports  

---

<h2>Expected Outcomes</h2>

- ✔️ Enhanced agricultural decision-making with real-time insights  
- ✔️ Accurate forecasting to plan for future production trends  
- ✔️ Improved resource allocation through comparative analytics  
- ✔️ Scalable platform adaptable to new datasets and regions  
- ✔️ Professional reporting for stakeholders and policymakers  

---

<h2>Technical Manual</h2>

- <b>Prerequisites:</b> Python 3.8+, pip, Git, Chrome/Firefox/Edge browser  
- <b>Installation:</b>  
  <pre>
  pip install dash pandas plotly reportlab
  </pre>  
- <b>Run the App:</b>  
  <pre>
  python app.py
  </pre>  
- <b>Files Overview:</b>  
  - app.py → Main Dash app (layout, callbacks, processing)  
  - components/layout.py → UI layout and tab structure  
  - components/export_reports.py → Export and reporting logic  
  - utils/data_loader.py → Data loading and preprocessing  
  - assets/style.css → Custom CSS styles  
  - agri_analysis_punjab_clean.csv → Dataset (Year, Season, Area, Burned Area, Difference, % Difference)  

---

<h2>Conclusion</h2>
The Hydrolytix Agri Intelligence Dashboard redefines agricultural analytics by combining modern web technologies with forecasting and reporting tools. Through its modular design, interactive interface, and export features, it empowers researchers, policymakers, and farmers with the insights needed for sustainable agricultural planning and improved productivity.
