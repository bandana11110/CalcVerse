import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

import pytesseract
from PIL import Image
import sympy as sp
from statistics import mean, median


st.set_page_config(
    page_title="CalcVerse",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 CalcVerse")

st.markdown(
    """
    ### Welcome to CalcVerse
    Your all-in-one platform for:
    - 🧮 Scientific Calculations
    - 📈 Graph Plotting
    - 📊 Statistical Analysis
    - 🧠 Equation Solving
    - 📜 Calculation History
    """
)


from calculator_engine import calculate
from database import (
    create_db,
    save_history,
    get_history
)

create_db()

menu = st.sidebar.selectbox(
    "Choose Tool",
    [
        "Scientific Calculator",
        "Graph Plotter",
        "Statistics",
        "Equation Solver",
        "OCR calculator",
        "History"
    ]
)

if menu == "Scientific Calculator":

    expression = st.text_input(
        "Expression",
        "sqrt(144)"
    )

    if st.button("Calculate"):

        try:

            result = calculate(expression)

            st.success(result)

            save_history(
                expression,
                result
            )

        except Exception as err:

            st.error(err)


elif menu == "Graph Plotter":

    expr = st.text_input(
        "Function",
        "x**2"
    )

    x = np.linspace(-10,10,500)

    try:

        y = eval(
            expr,
            {
                "x":x,
                "np":np
            }
        )

        df = pd.DataFrame({
            "x":x,
            "y":y
        })

        fig = px.line(
            df,
            x="x",
            y="y"
        )

        st.plotly_chart(fig)
        save_history(
            expr,
            "graph generated"
        )

    except:
        st.error("Invalid Function")


elif menu == "Statistics":

    data = st.text_area(
        "Enter numbers separated by commas"
    )

    if st.button("Analyze"):

        numbers = []

        for i in data.split(","):

            value = float(i.strip())

            numbers.append(value)            
        

        st.write("Mean:",mean(numbers))
        st.write("Median:",median(numbers))
        st.write("Max:",max(numbers))
        st.write("Min:",min(numbers))
        st.write("Std Dev:",np.std(numbers))

        mean_value = mean(numbers)
        median_value = median(numbers)
        max_value = max(numbers)
        min_value = min(numbers)
        std_value = np.std(numbers)

        save_history(
            data,
            "Mean=" + str(mean_value) +
            ", Median=" + str(median_value) +
            ", Max=" + str(max_value) +
            ", Min=" + str(min_value) +
            ", Std=" + str(std_value)
        )


elif menu == "Equation Solver":

    equation = st.text_input(
        "Equation",
        "x**2+5*x+6"
    )

    if st.button("Solve"):

        x = sp.symbols("x")

        expression = sp.sympify(
            equation
        )

        solution = sp.solve(
            expression,
            x
        )

        st.success(solution)
        save_history(
            equation,
            solution
        )


elif menu == "OCR calculator":
    st.subheader("📸 OCR calculator")

    uploaded_file = st.file_uploader(
        "Upload an image containing a math expression",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)

        st.image(image, caption="Uploaded Image")

        try:
            text = pytesseract.image_to_string(image)

            st.success(f"Detected Expression: {text}")

            expression = text.strip()

            result = eval(expression)

            st.success(f"Answer = {result}")

        except:
            st.error("Could not solve expression.")




elif menu == "History":

    st.subheader("📜 Calculation History")

    data = get_history()

    if not data:
        st.info("No calculations yet.")

    else:

        for expression, result in data:

            st.write(
                f"🧮 {expression} = {result}"
            )