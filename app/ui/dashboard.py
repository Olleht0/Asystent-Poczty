import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Email Assistant",
    page_icon="📧",
    layout="wide",
)

st.title("📧 Email Assistant")
st.caption("Inteligentny asystent poczty elektronicznej")

tab1, tab2 = st.tabs([
    "📥 Skrzynka odbiorcza",
    "➕ Dodaj wiadomość",
])

with tab1:
    st.subheader("Odebrane wiadomości")

    try:
        response = requests.get(
            f"{API_URL}/emails",
            timeout=10,
        )
        response.raise_for_status()
        emails = response.json()

        if not emails:
            st.info("Brak wiadomości w bazie danych.")

        for email in emails:
            with st.expander(
                f"📩 {email['subject']} — {email['sender']}"
            ):
                st.write(f"**Od:** {email['sender']}")
                st.write(
                    f"**Data:** {email['received_at']}"
                )
                st.divider()
                st.write(email["body"])

                st.button(
                    "🤖 Analizuj przez AI",
                    key=f"analyze_{email['id']}",
                    disabled=True,
                    help="Funkcja dostępna w kolejnym etapie",
                )

    except requests.RequestException as error:
        st.error(
            "Nie udało się połączyć z FastAPI. "
            "Sprawdź, czy backend działa."
        )
        st.caption(str(error))


with tab2:
    st.subheader("Nowa wiadomość testowa")

    with st.form("email_form"):
        sender = st.text_input("Nadawca")
        subject = st.text_input("Temat")
        body = st.text_area("Treść wiadomości")

        submitted = st.form_submit_button(
            "Zapisz wiadomość"
        )

        if submitted:
            if not sender.strip() or not subject.strip() or not body.strip():
                st.warning("Wypełnij wszystkie pola.")
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/emails",
                        json={
                            "sender": sender,
                            "subject": subject,
                            "body": body,
                        },
                        timeout=10,
                    )
                    response.raise_for_status()

                    st.success(
                        "Wiadomość została zapisana!"
                    )

                except requests.RequestException as error:
                    st.error(
                        "Nie udało się zapisać wiadomości."
                    )
                    st.caption(str(error))