import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Puslapio antraštė
st.title("Automatizacijos naudos skaičiuoklė")

st.write("""
Sužinokite, kiek laiko ir pinigų galite sutaupyti automatizavę savo verslo procesus!
""")

# Maža instrukcija vartotojui
with st.expander("📖 Kaip naudotis skaičiuokle?"):
    st.markdown("""
    1. Pasirinkite, kiek darbuotojų naudos automatizaciją.
    2. Įveskite kiekvieno darbuotojo:
      - Sutaupytas darbo dienas per mėnesį
      - Jo valandinį atlyginimą (€)
    3. Nurodykite darbo dienų skaičių per mėnesį.
    4. Įveskite bendrą investicijos sumą į automatizaciją (€), jei žinoma.
    5. Peržiūrėkite rezultatus ir atsisiųskite skaičiavimą Excel formatu.
    """)

# Įvedimai
number_of_employees = st.number_input("Kiek darbuotojų naudos automatizaciją?", min_value=1, step=1, value=1)

st.markdown("### Įveskite kiekvieno darbuotojo duomenis:")
days_saved_list = []
hourly_wage_list = []

for i in range(1, number_of_employees + 1):
    st.markdown(f"**Darbuotojas {i}**")
    days = st.number_input(f" - Sutaupyta darbo dienų per mėnesį (1 darbo diena = 8 valandos)", min_value=0.0, step=0.5, key=f"days_{i}")
    wage = st.number_input(f" - Valandinis atlyginimas (€)", min_value=1.0, step=0.5, key=f"wage_{i}")
    days_saved_list.append(days)
    hourly_wage_list.append(wage)

working_days_per_month = st.number_input("Darbo dienų skaičius per mėnesį", min_value=1, max_value=31, value=20)
investment_cost = st.number_input("Investicijos suma į automatizaciją (€)", min_value=0.0, step=10.0, value=0.0)

# Skaičiavimai
hours_saved_per_month_total = 0
money_saved_per_month_total = 0

for days, wage in zip(days_saved_list, hourly_wage_list):
    if working_days_per_month > 0:
        minutes_saved_per_day = (days * 480) / working_days_per_month
    else:
        minutes_saved_per_day = 0

    hours_saved_per_month = (minutes_saved_per_day * working_days_per_month) / 60
    money_saved_per_month = hours_saved_per_month * wage

    hours_saved_per_month_total += hours_saved_per_month
    money_saved_per_month_total += money_saved_per_month

hours_saved_per_year_total = hours_saved_per_month_total * 12
money_saved_per_year_total = money_saved_per_month_total * 12

# 3 ir 5 metų apskaičiavimai
money_saved_3_years = money_saved_per_year_total * 3
money_saved_5_years = money_saved_per_year_total * 5

# Rezultatai
st.subheader("Rezultatai:")

st.write(f"**Bendrai sutaupyta darbo dienų per mėnesį:** {sum(days_saved_list):.2f} dienos")
st.write(f"**Per mėnesį sutaupoma:** {hours_saved_per_month_total:.2f} valandos / {money_saved_per_month_total:.2f} €")
st.write(f"**Per metus sutaupoma:** {hours_saved_per_year_total:.2f} valandos / {money_saved_per_year_total:.2f} €")
st.write(f"**Per 3 metus sutaupoma:** {money_saved_3_years:.2f} €")
st.write(f"**Per 5 metus sutaupoma:** {money_saved_5_years:.2f} €")

# ROI skaičiavimas
if investment_cost > 0:
    roi = ((money_saved_per_year_total - investment_cost) / investment_cost) * 100
    st.write(f"**Investicijos grąža (ROI):** {roi:.2f}% per pirmus metus")
else:
    st.info("Investicijos suma nenurodyta. Visi sutaupyti pinigai – grynasis pelnas!")

# Motyvacinė žinutė
st.success("🎯 Matote, kiek daug galite sutaupyti! Nedelskite – diekite automatizaciją jau šiandien ir stiprinkite savo verslą! 🚀")

# Grafikas - stulpelinė diagrama
st.subheader("Sutaupytų pinigų augimas per metus:")

months = [f"{i}-mėn." for i in range(1, 13)]
money_saved_cumulative = [money_saved_per_month_total * i for i in range(1, 13)]

plt.figure(figsize=(10, 6))
plt.bar(months, money_saved_cumulative)
plt.xlabel('Mėnuo')
plt.ylabel('Sutaupyta suma (€)')
plt.title('Automatizacijos naudos augimas per metus')
plt.xticks(rotation=45)
plt.grid(axis='y')
st.pyplot(plt)

# Failo paruošimas parsisiuntimui
st.subheader("Atsisiųskite savo skaičiavimą:")

df = pd.DataFrame({
    'Mėnuo': months,
    'Sutaupyta suma (€)': money_saved_cumulative
})

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Nauda')
    processed_data = output.getvalue()
    return processed_data

excel_data = convert_df_to_excel(df)

st.download_button(
    label="📥 Atsisiųsti Excel failą",
    data=excel_data,
    file_name='automatizacijos_nauda.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# Call to Action - gražus mygtukas
st.markdown("""
<br>
<div style="text-align: center;">
    <a href="https://sigitasprendimai.lt/kontaktai-susisiekti/" target="_blank" style="background-color: #4CAF50; 
       color: white; padding: 15px 32px; text-align: center; text-decoration: none; 
       display: inline-block; font-size: 16px; border-radius: 8px;">🚀 Susisiekti dabar</a>
</div>
<br>
""", unsafe_allow_html=True)

st.caption("Pasinaudokite automatizacijos galimybėmis ir stiprinkite savo verslą jau šiandien!")
