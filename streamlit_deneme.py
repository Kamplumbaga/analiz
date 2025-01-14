import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit başlığı
st.title("Kelime Trend Analizi")

# Excel dosyası yükleme
uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

if uploaded_file:
    # Excel dosyasını okuma
    data = pd.read_excel(uploaded_file)

    # Veriyi temizleme ve hazırlama
    data['tarih'] = pd.to_datetime(data['tarih'], errors='coerce')  # 'tarih' sütununu datetime formatına çevirme
    data['Frekans'] = pd.to_numeric(data['Frekans'], errors='coerce')  # 'Frekans' sütununu numerik yapma

    # Pivot data for plotting
    pivot_data = data.pivot_table(index='tarih', columns='Kelime', values='Frekans', aggfunc='sum')

    # Tüm kelimelerin trend grafiği
    st.subheader("Tüm Kelimelerin Trend Grafiği")
    fig, ax = plt.subplots(figsize=(15, 7))

    for word in pivot_data.columns:
        ax.plot(pivot_data.index, pivot_data[word], label=word)
        # Grafiğin sonuna kelime etiketi ekleme
        if not pivot_data[word].isna().all():
            ax.text(pivot_data.index[-1], pivot_data[word].iloc[-1], word,
                    fontsize=9, color=ax.lines[-1].get_color())

    ax.set_title("Kelime Trendleri (Etiketli)", fontsize=16)
    ax.set_xlabel("Tarih", fontsize=12)
    ax.set_ylabel("Frekans", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Selectbox ile kelime seçimi
    st.subheader("Kelimeye Göre Trend Grafiği")
    selected_word = st.selectbox("Bir kelime seçin", options=pivot_data.columns)

    # Seçilen kelimenin trend grafiği
    if selected_word:
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.plot(pivot_data.index, pivot_data[selected_word], label=selected_word, color='blue')
        ax.set_title(f"{selected_word} Kelimesinin Trend Grafiği", fontsize=16)
        ax.set_xlabel("Tarih", fontsize=12)
        ax.set_ylabel("Frekans", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)
