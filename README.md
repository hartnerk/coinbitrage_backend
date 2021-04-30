# Coin bitrage backend

Using cryptowat.ch and twilio API to pull prices of coins and compare across  exchanges and to send messages when a percent difference threshold is met.  Django used for back end. Auth uses JWT tokens (get http://localhost:8000/token-auth/ )

BASE_URL = 'http://localhost:8000/coinbitrage_api';

getAlertByID=() => fetch( (`${BASE_URL}/get_alert_by_id/${alert_id}`)

deleteAlert= (id, token) => fetch(`${BASE_URL}/alerts/${id}/delete`)

editAlert= (AlertObject, alert_id, token) => fetch(`${BASE_URL}/alerts/${alert_id}/edit`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `JWT ${token}`
      },
      method: "POST",
      body: JSON.stringify(AlertObject)
    });

addAlert= (AlertObject, token) => (
      return fetch(`${BASE_URL}/alerts/new`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `JWT ${token}`
      },
      method: "POST",
      body: JSON.stringify(AlertObject)
    });

getSpreads = async (coin_name, token)=.( fetch(`${BASE_URL}/coinio/${coin_name}/best`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `JWT ${token}`
      }
    })
    const data = await response.json();
    console.log('CoinOIAPI returned data',data  )
    return data
  });

