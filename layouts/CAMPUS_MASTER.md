# Semiconductor Campus Master

> Last validated: 2026-10-22 · Maintainer: Mandata

Korean semiconductor campuses covered by Mandata's zone layouts. Column names and formats follow the `ZONE_MASTER` schema in [ZONE_LAYOUTS.md](ZONE_LAYOUTS.md).

| company_name_en | security_code | campus_name | campus_code | campus_address |
| --- | --- | --- | --- | --- |
| SK HYNIX INC | KR7000660001 | ICHEON | SKH_ICH | 2091, Gyeongchung-daero, Bubal-eup, Icheon-si, Gyeonggi-do (17336) |
| SK HYNIX INC | KR7000660001 | CHEONGJU | SKH_CJJ | 215, Daesin-ro, Heungdeok-gu, Cheongju-si, Chungcheongbuk-do (28429) |
| SK HYNIX INC | KR7000660001 | YONGIN | SKH_YIN | Wonsam-myeon, Cheoin-gu, Yongin-si, Gyeonggi-do |
| SAMSUNG ELECTRONICS CO LTD | KR7005930003 | GIHEUNG | SSE_GHG | 1, Samsung-ro, Giheung-gu, Yongin-si, Gyeonggi-do (17113) |
| SAMSUNG ELECTRONICS CO LTD | KR7005930003 | HWASEONG | SSE_HWA | 1, Samsungjeonja-ro, Hwaseong-si, Gyeonggi-do (18448) |
| SAMSUNG ELECTRONICS CO LTD | KR7005930003 | PYEONGTAEK | SSE_PTK | 114, Samseong-ro, Pyeongtaek-si, Gyeonggi-do (17786) |
| SAMSUNG ELECTRONICS CO LTD | KR7005930003 | CHEONAN | SSE_CAN | 465, Beonyeong-ro, Seobuk-gu, Cheonan-si, Chungcheongnam-do (31086) |
| SAMSUNG ELECTRONICS CO LTD | KR7005930003 | ONYANG | SSE_ONY | 158, Baebang-ro, Baebang-eup, Asan-si, Chungcheongnam-do (31489) |

## Column notes

- **`company_name_en`:** the registered English name, written in upper case with no punctuation (`SK hynix Inc.` → `SK HYNIX INC`; `Samsung Electronics Co., Ltd.` → `SAMSUNG ELECTRONICS CO LTD`).
- **`security_code`:** the ISIN of the listed common share (KRX tickers `000660` and `005930`).
- **`campus_code`:** `<company prefix>_<campus>`, where `SKH` = SK hynix and `SSE` = Samsung Electronics.
- **`campus_address`:** the English road-name address, with the postal code in brackets.

## Campus notes

- **SKH_ICH (Icheon):** this is also SK hynix's registered head office.
- **SKH_CJJ (Cheongju):** the address is Cheongju Plant 1. SK hynix runs 3 more plants in Cheongju:
  - Plant 2: 959, 2sunhwan-ro, Heungdeok-gu (Hyangjeong-dong)
  - Plant 3: 337, Jikji-daero, Heungdeok-gu (Hyangjeong-dong)
  - Plant 4: 120, SK-ro, Heungdeok-gu (Oebuk-dong)
- **SKH_YIN (Yongin):** the Yongin semiconductor cluster in Dokseong-ri, Godang-ri and Jukneung-ri (Wonsam-myeon) is still under construction, so it has no road-name address yet.
- **SSE_GHG and SSE_PTK:** both roads are 삼성로 in Korean. Samsung's own certificate spells the Giheung road `Samsung-ro` and the Pyeongtaek road `Samseong-ro`, and the table keeps both spellings as published.
- **SSE_CAN (Cheonan) and SSE_ONY (Onyang):** these are assembly, test and packaging sites. Onyang is in Asan (Baebang-eup), even though the campus is named after Onyang.

## Sources

- Samsung Electronics semiconductor ISO 45001 certificate, which lists all 5 Samsung plant addresses (issued 2024-12-13): <https://download.semiconductor.samsung.com/resources/others/ISO_45001.pdf>
- SK hynix head office address: <https://www.skhynix.com/sustainability/UI-FR-SA1601/>
- SK hynix Cheongju plant addresses: <https://ko.wikipedia.org/wiki/SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4>
- Cheongju postal code 28429 (a business at the same 215 Daesin-ro address): <https://www.bsigroup.com/en-IE/validate-bsi-issued-certificates/client-directory-profile/QRT_SE-0047347753-002>
- ISINs: <https://www.justetf.com/uk/stock-profiles/KR7000660001>, <https://www.justetf.com/uk/stock-profiles/KR7005930003>
