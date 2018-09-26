# Lonja
Script and documentation referred to the Lonja project

This project consists in deploy and configure a system that downloads a html document from one web site (one online store called "delalonjaalamesa"), does web-scrapping for obtaninig products and prices and stores all values in a TSDB. After that, it's possible ask for de the products and prices across a Grafana GUI.  The code and the instructions for deploy it (documentation folder) is valid for Linux and Raspbian systems.

The system is based in the technologies/components related below:

1. Python -> The programming language used for the develop.
2. Graphite -> The TSDB (Time Series Data Base) used for storing and ask for the metrics (products and prices).
3. Grafana -> The GUI used for visualizing the data.
