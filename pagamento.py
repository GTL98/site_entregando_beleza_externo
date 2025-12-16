# --- Importar as bibliotecas --- #
import mercadopago
import streamlit as st


def pagamento():
    """Função responsável por realizar o pagamento da compra."""
    # --- Obter o carrinho de pagamento --- #
    carrinho = st.session_state.cliente

    # --- Lista com os itens --- #
    itens = []

    # --- Separar as informações de compra --- #
    for produto, quantidade, codigo, valor_unitario in zip(carrinho['produtos'], carrinho['quantidade'], carrinho['codigos'], carrinho['valor_unitario']):
        itens.append(
            {
                'title': f'{produto} ({codigo})',
                'id': str(codigo),
                'quantity': quantidade,
                'unit_price': valor_unitario,
                'currency_id': 'BRL'
            }
        )

    # --- API da conta --- #
    sdk = mercadopago.SDK("APP_USR-8924499435607473-090309-70b3c32609e2ce6c0f6d2f73a01827d7-2665440960")

    # --- Configurações --- #
    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
    }

    # --- Dicionário com as informações da compra --- #
    payment_data = {
        'items': itens
    }

    # --- Realizar a chamada para a geração do link de pagamento --- #
    result = sdk.preference().create(payment_data, request_options)
    payment = result["response"]['init_point']

    # --- Mudar para a página de pagamento ---- #
    st.session_state.compras = {'produtos': 0}
    st.link_button(
        label='Ir ao Mercado Pago',
        url=payment,
        use_container_width=True
    )
