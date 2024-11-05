# Analysis of the presence of potential endocrine disruptors in personal care products and color cosmetics.
![image](https://github.com/user-attachments/assets/595416fd-c4be-4963-8956-36d43a3c649c)

# Project Objective
Understanding the current state of regulation regarding the presence of endocrine disruptors in various cosmetic and makeup products, as well as analyzing the composition of formulations to gain insight into this issue.

# Project Overview
To tackle the challenge of identifying potential endocrine disruptors in cosmetic products, we discovered the Sephora website as a valuable resource. We aim to leverage web scraping techniques to:
·Refine our product selections
·Enhance safety and awareness regarding various chemical substances
·Ensure informed decision-making by cross-referencing findings with the official ECHA list of endocrine disruptors
This approach will enable us to deepen our understanding of these chemical substances while promoting informed choices and prioritizing consumer safety.

# Analysis Methodology
**Step 1: Obtaining the data to work with. Using web scrapping methodologies**
 1.1: Utilizing Selenium to extract URLs from Sephora's Spanish Website for three selected categories: Body, Treatment and Make-up<br>
 1.2: Extracting Information with Beautiful Soup from URLs. <br>Fields to obtain: category, subcategory product name, brand name, rating, review count, price, and ingredients.<br>
**Step 2: Cleaning the dataframe, handle null values and formatting**<br>
**Step 3: Found the endocrine disruptors inside the ingredients column**
Since we couldn't find any results using the official list of endocrine disruptors from ECHA (https://www.echa.europa.eu/es/ed-assessment), 
we consulted various research studies to develop our own list of potential endocrine disruptors. This will allow us to identify matches within our dataframe in the possible future.<br>
**Step 4: Answer our research questions-stated below**<br>
  4.1 Question 1: Number of products per category and subcategory that contain endocrine disruptors.<br>
  4.2 Question 2: Which categories and brands have the most endocrine disruptors?<br>
  4.3 Question 3: Is there any relationship between the economic value and the number of endocrine disruptors? <br>Do more expensive brands contain fewer disruptors, while cheaper brands contain more?<br>
  4.4.Question 4: Are consumers aware of endocrine disruptors in cosmetic products?Do they consider them in their product reviews? How does the average rating correlate with the presence of endocrine disruptors?<br>
  4.5 Question 5: What are the top 5 endocrine disruptors in this sample for each category? Is there any difference?<br>

# Conclusions on Endocrine Disruptors in Cosmetics
In our sample, we found a low presence of endocrine disruptors, with only 11.6% of the analyzed products containing these compounds. It is important to note that Europe has stringent legislation regarding chemicals, and some of the identified ingredients are already restricted or banned under the REACH regulation.

However, in the makeup category, we identified more potential endocrine disruptors, especially when analyzing heavy metals used in pigments.

A key finding is that the price of products does not appear to correlate with the presence of endocrine disruptors. While price may influence the quality of active ingredients, fragrances, and other components, this does not necessarily mean that the chemical risk is lower.

Another significant point is that consumers lack knowledge about the chemical composition of products and the risks associated with many ingredients. This is even more relevant regarding endocrine disruptors, as there is currently no official classification for their regulation in cosmetics. However, a new CLP regulation is expected to come into effect, which will include endocrine disruptors as a category of hazard.

Identified Endocrine Disruptors:
Octocrylene
Benzophenone-3
Parabens
These compounds have shown evidence of hormonal effects, although the magnitude and relevance of these effects may vary.

Compounds Not Considered Endocrine Disruptors:
Zinc
Manganese
Barium
Copper
While these elements are not considered endocrine disruptors, excessive exposure can pose other health risks.

