import pandas as pd
import streamlit as st
import requests

id:list = [29975197,63707237,63712502,63710448,18929193,18899796,18918115,63692128,18930121,18930040,63686895,63708463,18829924,63693382,63680677,18928488,18910945,18913190,18804248,18826209,18826293,18827762,29960113,63655099,18894038,18780660,18937145,18795393,18931674,18826321,63657872,18931121,18645447,18645512,18744647,18882861,18758208,63649955,18649434,18640920,29942893,18766717,18631126,18780529,63624809,18764258,18675472,63620911,63550058,18575885,18706850,18598007,18735103,18601482,18616709,18733868,18595501,63617449,63617447,63548233,18964474,18822328,18906188,63543077,18604632,18381670,18629994,18634906,18634902,18925120,18501302,18480009,18607861,18383058,18383066,18528829,18482160,18513595,18510668,18231661,18238546,63525178,18764455,18920941,18901733,18236977,18236964,18383062,18433489,18815467,18408863,18227998,18218134,18366708,18502116,18510728,18529020,63458463,17402970,18509381,18524393,18210118,18664966,18665138,29889486,29889482,29908394,18432098,18432096,18132471,18608357,18189407,18408833,29908408,18142610,18168353,63439886,18186153,18215207,18089753,18502014,18502016,18104982,18104976,18130435,18130433,18054873,17979039,17979026,18052918,18052919,29866098,17899054,17902459,29865201,17941689,17941699,17942306,18130916,17940780,17822786,17959114,17933441,17896903,17954229,17945272,17941209,18086959,29864348,17887288,18218966,17885540,18203668,18115865,17883830,17662226,17883847,18350459,18096039,29792361,17740257,17742814,17934541,17664392,29820796,17668395,17687964,17687975,29818810,17806273,17607102,17731568,17588464,17611992,17561603,17822785,17562415,17693549,17558921,17512238,17554140,17565238,17582716,17547679,17475162,17699118,17509003,17373845,17293917,17821168,18209520,17671275,16095770,17021772,16480134,17140186,16652208,17291309,17205017,16726852,17290761,16318868,17291315]
id = sorted(id)

if "data" not in st.session_state:
    st.session_state.data = []
if "error" not in st.session_state:
    st.session_state.error = []
if "mailRoomDates" not in st.session_state:
    st.session_state.mailRoomDates = []

if not st.session_state.data:
    try:
        data:list = []
        error:list[dict] = []

        for i in id:
            res = requests.get(f'https://ped.uspto.gov/api/queries/cms/public/{i}', verify=False)

            if res.status_code == 200:
                json = res.json()
                if json:
                    data.append(json[0])
            else:
                if res.status_code == 400:
                    error_message = f"錯誤代碼【{res.status_code}】: 參數錯誤"
                elif res.status_code == 401:
                    error_message = f"錯誤代碼【{res.status_code}】: 需驗證身分"
                elif res.status_code == 403:
                    error_message = f"錯誤代碼【{res.status_code}】: 過度請求導致封鎖"
                elif res.status_code == 404:
                    error_message = f"錯誤代碼【{res.status_code}】: 沒有資料"
                else:
                    error_message = f"預期外的錯誤代碼【{res.status_code}】"

                error.append({"error_id": str(i), "error_code": error_message })

        st.session_state.data = data
        st.session_state.error = error
        st.session_state.mailRoomDates = ["顯示全部"] + sorted(
            list(set(item.get("mailRoomDate", "未知日期") for item in data)),
            reverse=False
        )

    except Exception as e:
        st.markdown(f"### 發生錯誤：{e}")

data = st.session_state.data
error = st.session_state.error
mailRoomDates = st.session_state.mailRoomDates

with st.sidebar:
    add_selectbox = st.selectbox('mailRoomDates select', mailRoomDates)
    st.title(f"篩選日期：{add_selectbox}")

if add_selectbox == "顯示全部":
    selected_item = data
else:
    selected_item = [item for item in data if item.get("mailRoomDate") == add_selectbox]

st.markdown(f"共查到{len(selected_item)}/{len(id)}筆資料")
df = pd.DataFrame(data = selected_item)
st.dataframe(df, use_container_width=True)

if error:
    st.markdown("---")
    st.markdown(f"共{len(error)}筆回報錯誤的資料：")
    df = pd.DataFrame(error)
    st.dataframe(df, use_container_width=True)