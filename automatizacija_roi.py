import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Puslapio nustatymai
st.set_page_config(page_title="Automatizacijos naudos skaičiuoklė", page_icon="", layout="centered")

st.title("Sužinokite, kiek laiko ir pinigų galite sutaupyti automatizavę savo verslo procesus!")

st.header("Įveskite duomenis:")

# Įvesties laukai
num_employees = st.number_input("Kiek darbuotojų naudosis automatizacija?", min_value=1, value=1)

days_saved_per_employee = []
hourly_rates = []

for i in range(num_employees):
    with st.expander(f"Darbuotojas {i+1}"):
        days_saved = st.number_input(
            f"Kiek darbo dienų per mėnesį taupo automatizacija? (1 darbo diena = 8 valandos)",
            min_value=0.0,
            step=0.5,
            key=f"days_saved_{i}"
        )
        hourly_rate = st.number_input(
            f"Darbuotojo {i+1} valandinis atlyginimas (€)",
            min_value=0.0,
            value=7.0,
            step=0.5,
            key=f"hourly_rate_{i}"
        )
        days_saved_per_employee.append(days_saved)
        hourly_rates.append(hourly_rate)

working_days_per_month = st.number_input("Kiek darbo dienų yra per mėnesį?", min_value=1, value=21)

investment = st.number_input("Investicijos suma į automatizaciją (€)", min_value=0.0, value=0.0)

# ROI pasirinkimas su paaiškinimu
st.header("Investicijų grąžos (ROI) skaičiavimas")

st.markdown("""
**Kas yra ROI?**  
ROI (Return on Investment) – tai investicijų grąžos rodiklis, kuris parodo, kiek investuotos lėšos atsiperka kaip sutaupyti pinigai per pasirinktą laikotarpį.

**Kaip pasirinkti laikotarpį?**  
Pasirinkite, per kiek metų norite apskaičiuoti bendrą sutaupytą sumą ir grąžą:
- **1 metai** – matysite greitą efektą.
- **3 metai** – matysite vidutinės trukmės efektą.
- **5 metai** – matysite ilgalaikį efektą.
""")

roi_period_years = st.selectbox(
    "Pasirinkite laikotarpį ROI skaičiavimui:",
    (1, 3, 5),
    index=0
)

# Skaičiavimai
total_days_saved_per_month = sum(days_saved_per_employee)
total_hours_saved_per_month = total_days_saved_per_month * 8
total_value_saved_per_month = sum([(days * 8) * rate for days, rate in zip(days_saved_per_employee, hourly_rates)])

total_hours_saved_per_year = total_hours_saved_per_month * 12
total_value_saved_per_year = total_value_saved_per_month * 12
total_value_saved_3_years = total_value_saved_per_year * 3
total_value_saved_5_years = total_value_saved_per_year * 5
total_value_saved_all_years = total_value_saved_per_year * roi_period_years

if investment > 0:
    roi = ((total_value_saved_all_years - investment) / investment) * 100
else:
    roi = 1000

# Rezultatų rodymas
st.header("Rezultatai:")

st.write(f"**Bendras sutaupytų darbo dienų skaičius per mėnesį:** {total_days_saved_per_month:.2f} dienos")
st.write(f"**Per mėnesį sutaupoma:** {total_hours_saved_per_month:.2f} valandos / {total_value_saved_per_month:.2f} €")
st.write(f"**Per metus sutaupoma:** {total_hours_saved_per_year:.2f} valandos / {total_value_saved_per_year:.2f} €")
st.write(f"**Per {roi_period_years} metus sutaupoma:** {total_value_saved_all_years:.2f} €")
st.write(f"**Per 3 metus sutaupoma:** {total_value_saved_3_years:.2f} €")
st.write(f"**Per 5 metus sutaupoma:** {total_value_saved_5_years:.2f} €")

if investment > 0:
    st.write(f"**Investicijos grąža (ROI) per {roi_period_years} metus:** {roi:.2f}%")
else:
    st.info("Investicijos suma nenurodyta. Visi sutaupyti pinigai – grynasis pelnas!")

# Dinaminė žinutė pagal ROI
if roi >= 0:
    st.success(f" Puiku! Jūsų automatizacijos projektas per {roi_period_years} metus gali reikšmingai prisidėti prie išlaidų mažinimo ir verslo stiprinimo! ")
else:
    st.warning(f" Dėmesio: Per {roi_period_years} metus automatizacijos nauda nepadengia investicijų. Rekomenduojame peržiūrėti įvestus duomenis arba apsvarstyti papildomas optimizacijos galimybes.")

# Atsisiųsti Excel su grafiku
st.header("Atsisiųskite savo skaičiavimą:")

def convert_df_to_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df = pd.DataFrame({
            'Rodiklis': [
                "Per mėnesį sutaupoma (€)",
                "Per metus sutaupoma (€)",
                "Per 3 metus sutaupoma (€)",
                "Per 5 metus sutaupoma (€)"
            ],
            'Reikšmė': [
                total_value_saved_per_month,
                total_value_saved_per_year,
                total_value_saved_3_years,
                total_value_saved_5_years
            ]
        })

        df.to_excel(writer, index=False, sheet_name='Skaičiavimai')
        workbook = writer.book
        worksheet = writer.sheets['Skaičiavimai']

        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': 'Sutaupytos sumos',
            'categories': ['Skaičiavimai', 1, 0, 4, 0],
            'values': ['Skaičiavimai', 1, 1, 4, 1],
            'fill': {'color': '#1f77b4'}
        })
        chart.set_title({'name': 'Automatizacijos naudos analizė'})
        chart.set_x_axis({'name': 'Rodiklis'})
        chart.set_y_axis({'name': 'Suma (€)', 'min': 0})
        worksheet.insert_chart('D2', chart)

    output.seek(0)
    return output.getvalue()

excel_data = convert_df_to_excel()

st.download_button(
    label="📥 Atsisiųsti Excel failą su grafiku",
    data=excel_data,
    file_name="automatizacijos_skaiciavimas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Streamlit grafikas su skaičiukais virš stulpelių
st.header("Sutaupytų pinigų augimas per metus:")

months = [f"{i} mėn." for i in range(1, 13)]
monthly_growth = [total_value_saved_per_year * (i / 12) for i in range(1, 13)]

fig, ax = plt.subplots()
bars = ax.bar(months, monthly_growth, color='#1f77b4')
ax.set_title("Automatizacijos naudos augimas per metus")
ax.set_xlabel("Mėnuo")
ax.set_ylabel("Sutaupyta suma (€)")
plt.xticks(rotation=45)

for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f'{height:.0f} €',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 5),
        textcoords="offset points",
        ha='center',
        va='bottom',
        fontsize=8,
        color='black'
    )

st.pyplot(fig)

# Call to Action mygtukas
st.markdown(
    """
    <div style="text-align: center; margin-top: 2rem;">
        <a href="https://sigitasprendimai.lt/kontaktai-susisiekti/" target="_blank" rel="noopener">
            <button style="padding: 0.75em 1.5em; font-size: 1.2em; background-color: #28a745; color: white; border: none; border-radius: 10px; cursor: pointer;">
                 Susisiekti dabar
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

