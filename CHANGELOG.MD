# High Table Holdings Changelog

# High Table Holdings Changelog

## v3.7.0 - Enhanced User Experience and Transaction Accuracy

This release focuses on improving the overall user experience, refining the visual appearance, and ensuring the accuracy of financial calculations.

### User Interface Improvements:

- **Intuitive Search Bars:** Sales and account selection are streamlined with the introduction of searchable dropdowns. Instantly filter options as you type for a quicker and more user-friendly workflow. 
- **Modernized Design:** Elements now feature solid borders and refined layouts for a clean, modern aesthetic that aligns with current design trends.
- **Enhanced Listbox Navigation:** Seamlessly navigate through listbox suggestions using arrow keys, and easily make selections using the Enter key for a smoother workflow.

### Functionality Refinements:

- **Accurate Compound Interest Calculation:**  The interest calculation logic is revised to handle compound interest accurately, ensuring precise financial reporting, especially over extended periods.
- **Improved Account Balance Calculation:** Account balance computations are enhanced to correctly account for settlement transactions (Tag = 0) and apply compound interest only to unsettled periods, ensuring the displayed balance reflects the true financial status. 

### Technical Updates:

- **Introduction of `SearchBar` Component:**  Sales and account dropdowns leverage a new `SearchBar` component for a better user experience.
- **Visual Design Refinements:** Subtle updates across elements, including borders, fonts, and spacing, further polish the application's look and feel.

## Resolved Issues:

- **Accidental "0" Tags Fixed:** A potential data inconsistency issue is addressed where transactions were sometimes assigned a tag value of "0" unintentionally. Now, such accidental settings are automatically corrected during program startup, guaranteeing accurate reporting and balance calculation.

**Note:** This update might involve minor code changes and visual refinements across various modules to enhance overall software stability and maintainability. 

## v3.6.3 - Refined Bill and Report Management 

* **Full Bill Lifecycle Management:** You can now not only create and view bills but also fully modify and delete them using the `modifypage` module, providing granular control over your billing information.
* **Seamlessly Navigate to Edit with Ctrl+Click:** Productivity boost: Ctrl+clicking any row within the `reports` module swiftly redirects you to the `modifypage` with the corresponding row ready for editing.
* **Guaranteed Accurate Tax Calculations:** Addressed potential discrepancies in CGST/SGST calculations for bills. Tax amounts are now rounded off to two decimal places for consistent and precise billing.
* **Powerful Search Capabilities in Reports:** Locating specific entries is now simpler: Search functionality is enhanced in the `reports` module, enabling searches within table dropdowns by item/account names or dates across accounts, items, and daily pages.

## v3.6.2 - Streamlined User Onboarding 

* **Added Documentation for Smooth Start:**  New to High Table Holdings? You'll find detailed guidance in `documentation.md`, covering software setup, features, and how to get the most out of your experience.
* **Visualize with More Screenshots:** Multiple new screenshots highlight different themes and modules, giving you a clearer understanding of how High Table Holdings looks and functions.
    * accountslight
    * krardark
    * krarlight
    * modifydark
    * modifylight
    * saleslight
* **Enhanced README:** A friendlier and more informative welcome: The `readme.md` is updated with new screenshots, a more comprehensive project description, and links to the updated documentation.

## v3.6.1 - Optimized Visual Appeal and Accessibility 

* **Straightforward Project Intro:** Jump right in: The newly added `readme.md` gives you essential project information for quick setup and an immediate overview of the software. 
* **At-a-Glance UI Experience:** Get a visual preview of High Table Holdings with the new `screenshots` folder, displaying core interfaces and features before you even run the software.
* **Immersive Dark Theme:** Enhance focus: High Table Holdings launches with the dark theme active, ensuring a comfortable viewing experience that puts your data in the spotlight.

## v3.5.5 - Flexible Themes, Streamlined Transactions 

* **Introducing a Light Mode Choice:** Adjust High Table Holdings to your preferences: Enjoy a bright and user-friendly light theme alongside the classic dark theme. The convenient "@" label on the title bar makes switching effortless.
* **Theme Changes: Polished and Reliable:** Navigate through different modules (especially the homepage) with a smoother and more consistent experience as theme transitions are improved. 
* **Enhanced Reports for Precise Insights:** Quickly analyze your data with a newly designed format for displaying account reports. Clear column widths enhance readability for greater comprehension.

**Changes Not Directly Reflected in Changelog**

- **Performance Enhancements:** The software may show slightly faster load times and data processing speeds, likely due to internal code optimizations. 
- **Visual Design Tweaks:** You may notice subtle changes in element layouts, border styles, and overall visual refinement within some of the modules, further improving usability. 
- **Search Bar Upgrades:**  SearchBar elements seem to have added features like instant suggestion filtering, likely resulting from the use of a more specialized search bar component.  

**Notes**

- This changelog prioritizes visible changes that would matter to end users. Minor internal improvements or refactorings are not listed in detail unless they directly affect user interaction.  
- Changelog formatting aims for better clarity and conciseness. 