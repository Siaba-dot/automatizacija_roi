import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Automatizacijos naudos skaičiuoklė", page_icon="", layout="centered")

st.title("Sužinokite, kiek laiko ir pinigų galite sutaupyti automatizavę savo verslo procesus!")

st.header("Įveskite duomenis:")

num_employees = st.number_input("Kiek darbuotojų naudosis automatizacija?", min_value=1, value=1)

days_saved_per_employee = []
hourly_rates = []

for i in range(num_employees):
    with st.expander(f"Darbuotojas {i+1}"):
        days_saved = st.number_input(f"Kiek darbo dienų per mėnesį taupo automatizacija? (1 darbo diena = 8 valandos)", min_value=0.0, step=0.5, key=f"days_saved_{i}")
        hourly_rate = st.number_input(f"Darbuotojo {i+1} valandinis atlyginimas (€)", min_value=0.0, value=7.0, step=0.5, key=f"hourly_rate_{i}")
        days_saved_per_employee.append(days_saved)
        hourly_rates.append(hourly_rate)

working_days_per_month = st.number_input("Kiek darbo dienų yra per mėnesį?", min_value=1, value=21)

investment = st.number_input("Investicijos suma į automatizaciją (€)", min_value=0.0, value=0.0)

# Skaičiavimai
total_days_saved_per_month = sum(days_saved_per_employee)
total_hours_saved_per_month = total_days_saved_per_month * 8
total_value_saved_per_month = sum([(days * 8) * rate for days, rate in zip(days_saved_per_employee, hourly_rates)])

total_hours_saved_per_year = total_hours_saved_per_month * 12
total_value_saved_per_year = total_value_saved_per_month * 12
total_value_saved_3_years = total_value_saved_per_year * 3
total_value_saved_5_years = total_value_saved_per_year * 5

if investment > 0:
    roi = ((total_value_saved_per_year - investment) / investment) * 100
else:
    roi = 1000  # Jei investicija 0, ROI tiesiog didelis, bet perteikiam kitais žodžiais

st.header("Rezultatai:")

st.write(f"**Bendras sutaupytų darbo dienų skaičius per mėnesį:** {total_days_saved_per_month:.2f} dienos")
st.write(f"**Per mėnesį sutaupoma:** {total_hours_saved_per_month:.2f} valandos / {total_value_saved_per_month:.2f} €")
st.write(f"**Per metus sutaupoma:** {total_hours_saved_per_year:.2f} valandos / {total_value_saved_per_year:.2f} €")
st.write(f"**Per 3 metus sutaupoma:** {total_value_saved_3_years:.2f} €")
st.write(f"**Per 5 metus sutaupoma:** {total_value_saved_5_years:.2f} €")

if investment > 0:
    st.write(f"**Investicijos grąža (ROI):** {roi:.2f}% per pirmus metus")
else:
    st.info("Investicijos suma nenurodyta. Visi sutaupyti pinigai – grynasis pelnas!")

# Dinaminė žinutė
if roi >= 0:
    st.success("Sveikiname! Jūsų automatizacijos projektas gali reikšmingai prisidėti prie išlaidų mažinimo ir verslo stiprinimo!")
else:
    st.warning("Dėmesio: Šiuo atveju automatizacijos nauda nepadengia investicijų. Siūlome dar kartą peržiūrėti įvestus duomenis arba įvertinti papildomas optimizacijos galimybes.")

# Excel failo paruošimas
st.header("Atsisiųskite savo skaičiavimą:")

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Skaičiavimai')
    processed_data = output.getvalue()
    return processed_data

data = {
    "Rodiklis": [
        "Bendras sutaupytų darbo dienų skaičius per mėnesį",
        "Per mėnesį sutaupoma (valandos)",
        "Per mėnesį sutaupoma (€)",
        "Per metus sutaupoma (valandos)",
        "Per metus sutaupoma (€)",
        "Per 3 metus sutaupoma (€)",
        "Per 5 metus sutaupoma (€)",
        "Investicijos grąža (ROI)"
    ],
    "Reikšmė": [
        f"{total_days_saved_per_month:.2f}",
        f"{total_hours_saved_per_month:.2f}",
        f"{total_value_saved_per_month:.2f}",
        f"{total_hours_saved_per_year:.2f}",
        f"{total_value_saved_per_year:.2f}",
        f"{total_value_saved_3_years:.2f}",
        f"{total_value_saved_5_years:.2f}",
        f"{roi:.2f}%" if investment > 0 else "Nenurodyta"
    ]
}

df = pd.DataFrame(data)

excel_data = convert_df_to_excel(df)

st.download_button(
    label="📥 Atsisiųsti Excel failą",
    data=excel_data,
    file_name="automatizacijos_skaiciavimas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Call to Action
st.markdown(
    """
    <div style="text-align: center; margin-top: 2rem;">
        <a href="https://sigitasprendimai.lt/kontaktai-susisiekti/" target="_blank">
            <button style="padding: 0.75em 1.5em; font-size: 1.2em; background-color: #28a745; color: white; border: none; border-radius: 10px; cursor: pointer;">
                Susisiekti dabar
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
