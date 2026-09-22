#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import io
import json
import random
import re
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

APP_TITLE = "ASE 刷題練習"
BASE_DIR = Path(__file__).resolve().parent
WRONG_FILE = BASE_DIR / "wrong_questions.json"

QUESTIONS_PER_ROUND = 50
SCORE_PER_CORRECT = 2


QUESTION_BANK = r'''題目    正確答案
人力資源管理與發展並不包含教育訓練系統。    X
各部門的職場專業訓練(OJT)都是由人資處訓練部統一辦理的。 X
OJT即職場專業訓練，自各部門職涯藍圖發展而來，由各單位自行教導專業能力。 O
公司設定新進間接人員的訓練期為多久？ (A)1個月 (B)2個月 (C)3個月 (D)4個月    C
培育部屬是誰的責任？ (A)訓練單位 (B)直屬主管(部經副理) (C)公司負責人 (D)教育訓練委員會  B
"有關HRDS的敘述，下列何者錯誤？
(A)可得知公司內部最近有開辦哪些課程
(B)可得知自己最近應出席的課程
(C)可得知自己的必修課程(包含ASE學歷課程/OJT)
(D)以上皆是"    D
何者訓練不包含在間接人員的六大訓練體系中？ (A)間接新進訓練 (B)工程人員訓練 (C)部經/副理訓練 (D)OP資格複審訓練   D
"關於間接人員規劃之訓練體系有幾類？
(A)四
(B)五
(C)六
(D)七"  C
下列有關外訓與證照補助的描述何者正確？ (A)須經主管審核同意才可申請 (B)須與工作相關 (C)依補助費用而有不同綁約條款 (D)以上皆是    D
日月光的教育訓練理念之一為「直屬主管成為教導者」，所以G6員工在晉升主管的第一關須通過以下哪項課程? (A)主任管理基準 (B)內部講師培訓 (C)英語簡報 (D)經副理管理基準 B
ASE SPEC規格一般定期審核期限為二年。    O
EECN 重要(class 1)或主要(class 2)的變更只要工程師或主任簽核即可。   X
一旦納入文管中心的SPEC必須向DCC申請才可取得。   O
重要變更(class 1)或主要變更(class 2 )需經過 CCB 會議。  O
關於SPEC的變更，一旦經審核通過及生效相關的人、機、料、工皆必須配合，故發文者必須審慎與經過評估的。  O
SPEC的變更可以由經理發出的MEMO代替。    X
ASE SPEC編碼是由4組號碼組成「製程類別碼」編在第三組。   O
同一份TECN最多可延用三次。  X
ASE SPEC規格Control Plan定期審核期限為二年。    X
任何客戶的需求和規格，必須經過審核部門審核消化後轉換ASE內部規格讓相關同仁執行。 O
文件層級以1階文件為高指導原則，目前1階文件有4份，分別為品質手冊、環安衛管理手冊、企業社會責任管理手冊與日月光高雄廠資訊安全政策。   O
客戶規格審核需透過DCC發送給各部門審核，並視同合約必須確實審核。 O
TECN每次最長有效期為8週。   O
關於ASE SPEC的編碼別，第一組的第一碼為廠區別。  O
任何的部門與作業都必須有品質的觀念。    O
ASE SPEC規格S.P.C.定期審核期限為3個月。 O
ASE SPEC規格FMEA定期審核期限為： (A)2個月 (B)半年 (C)二年 (D)9個月  B
日月光變更文件ECN / TECN / EECN的第二組編碼代號依序分別為： (A)01／03／02 (B)01／02／03 (C)02／03／01 (D)03／02／01 B
同一份TECN最多可使用幾次？ (A)一次 (B)三次 (C)二次 (D)無限延用  B
工作時可根據以下何種文件來執行作業？ (A)SOP (B)MEMO (C)海報 (D)以上皆是 A
Critical/Major Change(重要變更和主要變更)在實施前，必須提出什麼文件並附上評估報告通知客戶？ (A)TECN (B)CRN (C)EECN (D)ECN   B
SPEC的變更必須透過何種文件審核程序？ (A)QCC (B)ECN (C)MRB (D)QDC    B
ASE SPEC編碼規格第四組號碼定義為何? (A)部門別 (B)文件階層 (C)流水號 (D)文件種頪 C
ASE SPEC編碼是由幾組號碼組成？ (A)3組 (B)2組 (C)4組 (D)1組  C
工程變更中下列何者為永久性變更通知，且版次須更新？ (A)EECN (B)CRN (C)FCN (D)ECN D
製造部或相關使用部門的 ASE SPEC 規格需由下列何部門公告才是合法的文件？ (A)IE (B)PE (C)HR (D)DCC D
有一材料其表面電阻值界於1.0x10^5Ω到1.0x10^9Ω之間，則該材料可視為消散性材質。    O
離子風扇正負電荷平衡值為 ≦ ± 50 V。 X
靜電鞋及靜電手環必須每日量測並確認通過後始可作業。  O
靜電服有破洞，為節省公司成本可以自行用針線予以修補。    X
消散性材質可以延長放電時間所以不用接地。    X
靜電防護步驟為︰不產生、不累積、不瞬間放電，以及生產機台環境內不要有帶電的電場。 O
不得以手(未帶抗靜電手套及手環)直接碰觸產品，若使用工具(鑷子、吸筆)接觸產品，該工具必須為認可之消散性材質工具。  O
靜電只有質子的正電荷，沒有電子的負電荷與中子的不帶電。  X
為求作業方便及快速，所以產品盤及靜電箱都可以不加上蓋子以方便取貨。  X
EPA管制靜電值為±50V以內且不得有絕緣體之物品(如紙張、計算機…)。  O
下列何者不是預防靜電放電的方法？ (A)避免電荷產生 (B)避免電荷累積 (C)用導體取代絕緣體 (D)降低放電速度。  C
人員靜電放電防護的方式為： (A)穿著靜電衣、鞋 (B)佩帶靜電手環 (C)戴靜電手套與手指套 (D)以上皆是  D
"靜電環上有限電流電阻，其目的為避免人員被漏電流電擊，該電阻阻值為：
(A) 0.8x10^2Ω~1.2x10^2Ω
(B) 0.8x10^6Ω~1.2x10^6Ω
(C) 0.8x10^10Ω~1.2x10^10Ω
(D) 0.8x10^14Ω~1.2x10^14Ω"  B
濕度與靜電兩者關係為何？ (A)有關係，濕度愈高靜電產生愈大 (B)有關係，濕度愈高靜電產生愈小 (C)無關係，濕度愈高靜電產生不變 (D)有關係，濕度對靜電影響小可以忽略    B
下列何者為ESD事件產生的模式？ (A)人體模式HBM (B)機器模式MM (C)元件充電模式CDM (D)以上皆是   D
人員已穿著靜電防護衣鞋後且量測通過後，則表示： (A)靜電已被適度抑制 (B)靜電不再發生 (C)與靜電無關 (D)以上皆非    A
在處理靜電敏感元件時，你應該： (A)遠離離子風扇 (B)在導電金屬表面工作桌作業 (C)戴上靜電手環及在有靜電消散保護工作桌面上作業 (D)以上皆非  C
"人員已穿著靜電防護衣鞋後並量測阻值通過始可進入EPA，該阻值通過門檻為：
(A)1.0x10^5 ≦ R < 3.5x10^7Ω
(B)7.5x10^5 ≦ R < 3.5x10^7Ω
(C)1.0x10^5 ≦ R < 1.0x10^7Ω
(D)7.5x10^5 ≦ R < 7.5x10^7Ω"    A
關於靜電消散材質的描述，以下何者為正確？ (A)可以將靜電絕緣 (B)不會因摩擦產生靜電 (C)可以延長靜電放電時間避免放電電流過大 (D)表面電阻值<1x10^5Ω  C
"關於靜電手環穿戴的描述，以下何者為正確？
(A)手環可束於靜電服袖子之上
(B)可以穿戴無線式手環
(C)靜電手環導電層必須與皮膚接觸並確認1MΩ接地線與接地端子已接妥
(D)手環應用夾子接地"    C
QIMS System成立改善小組最佳是4~10人，包括P.E、QA、ME、MFG等相關人員。   O
Quality Concern System是指QCS(外部)客戶抱怨系統(產品從客戶端發現問題)。 X
G8D與8D不同之處，是多了D0徵兆/ 緊急反應措施。   O
"依照QIMS System等級來分，依嚴重性排序何者正確？
(A)QA Dashboard>QCS>CCS
(B)CCS>QCS>QA Dashboard
(C)QCS>CCS>QA Dashboard
(D)QA Dashboard>CCS>QCS"    B
一份8D必須要於多少時間內完成？ (A)2天 (B)4天 (C)6天 (D)8天  B
G8D執行過程中是確認3D的效果，一份3D必須要於多少時間內完成？ (A)1天 (B)2天 (C)3天 (D)4天 A
QIMS(Quality Issue Management System)是指下列那些系統？ (A)CCS (B)QCS (C)QA Dashboard (D)以上皆是   D
若員工提出的案子，無具體可行之改善事項或人身攻擊之批評，皆是屬於不受理之提案。  O
只要提案是屬於受理的範圍，一職等到五職等的所有人員都可以提案。  X
提案主要目的是鼓勵基層員工發揮腦力激盪，提出具有建設性的創見，藉以改進研發、製程或管理能力，以及改善工作環境，並促進公司之經營能力及競爭力。    O
ID提案是將創意放在最適當的地方，並讓它產生效果。    O
創意是無中生有，創意並不是將現有的東西加以整合，使其形成與以往截然不同，甚至有更高產值的新事務。    X
所謂「提案制度」就是顧名思義要將「案」提出來，也就是將構想或意見、建議、希望等提出來。  O
請找出那一項提案是屬於不受理之提案？ (A)找出降低某站產品異常的方法 (B)機台錯料防呆系統線路改善 (C)成就幸福降低工作壓力 (D)降低材料或零組件損耗的方法    C
請找出那一項提案是屬於受理之提案？ (A)重覆性提案 (B)K2樓梯漏水、電燈壞掉 (C)產量多時常人手不足，增加儲備幹部人力 (D)負壓通道門增設警示燈，提醒出口門未完全關閉，造成設備損壞    D
提案獎金發放須通過哪一階主管審查？ (A)第一階段直屬主管(須部經副理級以上)初審 (B)第一階段直屬主管(須部經副理級以上)專案審查 (C)第二階段廠處長專案審查 (D)第三階段廠處長成果審查  A
何者為提案不受理的對象？ (A)一職等品質檢驗員 (B)四職等儲備組長 (C)五職等專案工程師 (D)五職等工程師  C
以下何者非提案改善的範圍： (A)機器設備與工具：如增加速度、簡化操作及器具之結構，降低維護費用及工具之改善等 (B)材料原物料：如節省材料、堆放庫存方式、縮短補給時間及成品包裝等 (C)員工福利、待遇、工會、福委會規章等公司規定與決策 (D)工作方法與效率：如操作方法改進、改善運動方法途徑、避免等待及簡化系統等  C
以下何者為提案改善的範圍： (A)引用他人專利及公司商標 (B)公知事實或主管已知範圍內、部門內改善或列入年度AOD之項目及相同內容者 (C)進行中 / 已完成規劃執行專案、部門內改善項目，不列入提案受理規定 (D)舊有被退件之建議，但有新資料可推翻原有審核意見者  D
以下何者非提案改善的對象： (A)專案工程師 (B)儲備組長 (C)工程師 (D)儲備幹部  A
申請IPO文件時，For ASE Group 關係人一律遵守「NO PO NO Action」 的原則。 O
IPO文件若帶出FOC No. (ex. AF-A0904028)，代表此IPO要收費。   X
IPO SOD到期日在IPO文件未Close(結案)前是可以延長的。 O
IPO SOD到期日計算是含假日的。   O
若IPO文件中，若欄位前有「*」標誌，則該欄位為必填欄位。  O
"IPO文件狀態為Initiator Working且SOD到期時，Issuer(開單者)確認該服務已結案後可以做哪些動作?
(A)進IPO系統做Close(結案)
(B)進IPO修改SOD日期
(C)進IPO系統做Cancel
(D)不理他"  A
若IPO SOD日到期後該IPO尚未Closed(結案)，系統會做何種通知？ (A)讓電腦自動當機 (B)每日由系統發mail通知Issuer (C)發出警鈴聲 (D)公告在佈告欄    B
IPO文件為何種狀態(Status)時Issuer(開單者)可以進系統將文件做Closed(結案)？ (A)Issue (B)WaitGR (C)InitiatorWorking (D)Approve Complete    C
何種服務可上IPO系統申請？ (A)實驗Service、Tooling、DesignService (B)廠內需求的事務清潔用品(ex.掃把、影印紙) (C)客戶來訪時所訂的餐飲 (D)以上皆可 A
IPO文件狀態為「WaitGR(WaitGoodReceive)」時，該IPO要如何才能轉成Closed(結案)？ (A)Issuer(開單者)於文件中按Closed按鈕 (B)系統串回GRNo後該IPO才轉Closed (C)每月底系統自動Close所有WaitGR的文件 (D)該IPO文件的SOD到期時就自動轉Close    B
品質是靠檢驗出來的，所以產品都要100%檢驗，以防不良品出給客戶。  X
TS16949強化客戶滿意度，故客戶需求與條文相違背時，須優先考慮客戶需求。   O
TS16949與ISO9001無關，此條文為汽車行業生產與服務之品質系統要求。    X
品質手冊是給高階主管以及客戶看的，一般員工不需要了解。  X
下列何者為ASE對品質的定義？ (A)出貨量愈高愈好 (B)SOD愈短愈好 (C)符合客戶需求標準 (D)作業人員於開心的情況下生產的產品    C
品質手冊為哪一個Level的文件？ (A)Level1 (B)Level2 (C)Level3 (D)Level4   A
烏龜圖中烏龜的身體(殼)，代表以下何者？ (A)Input輸入 (B)Output輸出 (C)Customersatisfaction客戶滿意 (D)Process過程    D
"內部稽核的目的，主要是確認品質系統符合下列何者？(1)股東的利益 (2)條文的要求 (3)組織所制定的管理系統之要求 (4)品質系統是否獲得有效的實施與管理 (5)環保署的要求
(A)2,3,4 (B)2,4,5 (C)1,3,4 (D)1,4,5"    A
合約可以不經法務審閱，由員工自行代表公司簽署。  X
不論是來自於公司內部、客戶或供應商的相關文件、資料，身為日月光的員工都應該嚴格遵守保密義務。    O
與客戶或供應商溝通協調該案的合約相關問題時，可不須取得法務同仁同意，請對方公司直接和法務連絡。  X
公司所有合約文件都應該經過法務審閱。    O
機密等級D的資料屬可公開資料。   O
向法務處申請審閱法律文件時之應注意事項何者正確？ (A)需給予法務同仁一定時間審閱，不在簽約之際才提出 (B)須協助法務同仁了解該案件的背景資料 (C)除非須由雙方法務針對合約內容討論，否則不宜請對方直接和法務聯絡 (D)以上皆是  D
以下哪些文件應經過法務審閱？ (A)客戶合約 (B)和解書 (C)保證函 (D)以上皆是    D
若有合約審閱或需法務部門協力事務，應以郵件用Note信箱寄到哪裡？ (A)legal@aseglobal.com (B)justice@aseglobal.com (C)law@aseglobal.com (D)legal@usi.com.tw A
請排出集團法務處在審閱合約時的正確流程：(1)Legal Review (2)Review on Business Acceptance (3)Contract Provided to Legal Team (4)Request (5)Legal Approved (A)1→2→3→4→5 (B)4→3→2→1→5 (C)4→2→3→1→5 (D)4→1→2→3→5    C
集團法務處須負責哪些業務？(1)合約審閱 (2)法規更新 (3)訴訟 (4)爭端解決 (5)協助各部門解釋法規 (A)1,2,3,4 (B)1,2,3,5 (C)2,3,4,5 (D)1,2,3,4,5   D
請選出日月光高雄廠員工聘僱合約的保密義務：(1)未經公司事前書面同意，員工不得將全部或部分機密資料以任何方式向他人揭露。(2)於聘僱關係終止時或經公司要求，員工應立即返還所有取得或持有公司之機密資料，且不得擅自影印。(3)員工如違反保密條款之規定，公司得依其違反情節之輕重依人事規章處分，或不經預告終止與員工之聘僱契約。(4)客戶、供應商資料標示Security A、B、C也有保密義務。 (A)1,2,3 (B)2,3,4 (C)1,2,4 (D)1,2,3,4  D
日月光集團包含以下哪幾個公司？(1)日月光電子股份有限公司 (2)環隆電氣股份有限公司 (3)蘇州日月新半導體有限公司 (4)日月光封裝測試上海有限公司 (5)台灣福雷電子股份有限公司 (A)1,2,4,5 (B)1,3,4,5 (C)2,3,4,5 (D)1,2,3,4,5 D
Class 1 等級之變更處理要求定義為在變更實施前，須知會客戶並取得其書面核准方可實施之變更。    O
SPEC的變更可以以MEMO代替。  X
Class 4 等級的變更不需要經過JxT Team的審核，也不需要經過CCB的審核。 O
Class 5 等級的變更審查關卡最少，所以應儘量運用以提升變更審查的效率。    X
Class 3 等級的變更須提供CCB評估報告。   X
Class 5 Change之變更等級在實施前，下列處理要求何者正確？ (A)不須通知客戶 (B)通知客戶且取得客戶同意 (C)通知客戶但不須取得客戶同意 (D)以上皆非    A
重複性相同(過去已有經驗值可供參考，不會動到產品之外觀、尺寸、功能、可靠度，並且沒有客戶特殊要求)的變更會是下列哪一等級的變更？ (A)Class 1 (B)Class 2 (C)Class 3 (D)Class 4  C
"Minor等級的變更不是屬於何種Class Level的變更？
(A)Class 2
(B)Class 3
(C)Class 4
(D)Class 5" A
"Major等級的變更，下列敘述何者正確？
(A)Major是屬於Class 1的等級變更
(B)不影響產品外觀、尺寸、功能、可靠性的變更
(C)不須提供評估報告
(D)以上皆非"    B
平均值與全距管制圖(X-R Chart)，屬於哪種管制圖？ (A)計量值管制圖 (B)計數值管制圖 (C)缺點數管制圖 (D)不良率管制圖 A
"關於QC7工具，下列何種情況不正確？(1)散布圖適用於計數型數據 (2)應用到80/20法則的是管制圖 (3)特性要因圖因形狀像魚骨又稱為魚骨圖 (4)查檢表按用途可分為查檢用與紀錄用
(A)1,3
(B)1,2
(C)2,4
(D)3,4" B
"下列何者不是直方圖的用途？
(A)明瞭數據整體概況
(B)可利用層別法比較數據差異
(C)監控品質特性
(D)發現數據異常"    C
當不知道兩個變數的關係或兩個變數之間的關係是比較模糊而需要進行調查與確認時，可通過何工具來確認二者之間的關係？ (A)柏拉圖 (B)魚骨圖 (C)散佈圖 (D)直方圖  C
管制圖的管制對象為下列何者？ (A)產品設計 (B)操作順序 (C)檢驗人員 (D)產品製程    D
哪一項是柏拉圖的錯誤看法？ (A)減少不良項目對整體的預設與評估 (B)各項目對整體所占份量及其影響程度為何 (C)問題大小排列一目了然 (D)哪一項目的問題最小  D
今某量產品發生問題，如分別以方法、機器、操作者、時間等加以觀察，此時可運用QC七大手法中何種方法收集可能的要因？ (A)散佈圖 (B)柏拉圖 (C)特性要因圖 (D)層別法  D
若產品發生問題的原因經過實驗確認後，發覺最有可能之要因是熱壓時間及強度兩者條件設定之問題，請問該運用QC七大手法中何種方法得知兩者之間之關係？ (A)柏拉圖 (B)查檢表 (C)魚骨圖 (D)散佈圖 (E)管制圖  D
在現場操作中出現品質問題時，作為品檢人員通常會使用查檢表記錄下其事件發生的具體情況及出現頻率或次數，以便後續追蹤。  O
管制圖常用來表示製程能力，並與規格界限比較，用以發現製程能否在規格界限內。  O
當一品質問題發生時，應確認問題，再通過4M1E即人、機、料、法、互不干涉五個環節進行分類，如有必要可再次细分至可以直接采取行动的方法是散佈圖。  X
柏拉圖常用來表現問題點，並呈現其相對重要性來提供改善方向的優先顺序。    O
管制圖中超出管制上下界線者即為不良品。  X
目前ASE總共管制55項有害物質，歐盟RoHS有害物質管制10項。 O
目前ASE日月光的產品可分為「Green」綠色產品和「Non-green」非綠色產品兩種。   O
ASE及SONY的「GP」 全名皆為Green Plant(綠色工廠)。   X
目前ASE只有「Flip Chip」產品符合Eu RoHS 排外條款。  O
SONY GP環保需求的Sony Document為FF-00259。  X
製程中若同時生產綠色產品以及非綠色產品，其中所使用的工具、工作桌、放置區皆不需分開標示、擺設與使用。    X
ASE「GP」意指的是： (A)綠色計劃 (B)綠色工廠 (C)綠色產品 (D)綠色製程 C
歐盟RoHS管控物質，以下何者為「非」？ (A)鎘 (B)鉛 (C)汞 (D)金    D
目前歐盟的RoHS法規，總共管制幾項有害物質？ (A)10項 (B)40項 (C)12項 (D)6項   A
"ASE進料管控措施針對綠色材料會以什麼顏色的標籤標示？
(A)紅色 (B)黃色 (C)藍色 (D)白色"    D
"以下何者不是歐盟RoHS 管控物質？
(A)鎘 (B)氯 (C)汞 (D)鉛"    B
ASE產品的定義以下選項何者正確？(1)綠色產品code''R''只能符合RoHS10項有害物質的要求 (2)非綠色產品的產品等級為code''H'' (3)綠色產品code''G''可以符合40項有害物質的要求 (4)ASE產品分為綠色產品及非綠色產品 (5)非綠色產品不能符合歐盟RoHS的需求 (A)3,4,5 (B)1,4,5 (C)2,3,5 (D)2,4,5  B
績效考核目標必須被「清楚、明白」的告知當事人，考核者與被考核者必須達成共識訂定目標。    O
所謂績效考核需「清楚、明白」的告知當事人，指「他被期待要作什麼」而非「他被期待要作到什麼程度」 。   X
績效考核的表單格式統一，各評量項目比重不因職務與職等而異。  X
績效考核結果由主管決定即可，不需與員工面談。    X
績效考核個人之目標設計必須和部門及公司之目標一致並可結合，重要的指標甚至由主管的AOD指標往下展開而成。   O
績效考核的目的為何： (A)回饋個人工作狀況並協助主管了解所屬工作表現 (B)作為員工訓練與生涯規劃之參考依據 (C)結合人事激勵系統，拔擢優秀員工並留攬人才 (D)以上皆是  D
績效考核參與對象範圍： (A)上半年度1-6月，為去年9/30(含)前到職之人員 (B)下半年度7-12月，當年度3/31(含)前到職之人員 (C)正式員工 (D)以上皆是   D
以下何者並非考績效考核對象： (A)未滿3個月的新人 (B)經/副理 (C)廠/處長 (D)總經理 A
貨品攜出加工區，需憑何種單據始可出區？ (A)E-SHIPPING單 (B)日月光半導體物品攜出證明單 (C)放行單 (D)廠商出貨單    C
"機台上的名牌有哪二個資料一定要於接收後七天內做確認，如有錯誤要立即反應予進口和收料單位？
(A)機台的型號&序號
(B)製造商&製造日期
(C)產地&合格認証標籤
(D)進口班機&船運資料"   A
進出區相關作業未符合海關及管理相關規定，依法可以論處的方式為何： (A)警告 (B)處新臺幣三萬元以上十五萬元以下罰鍰 (C)停止其一個月以上一年以下貨品之輸出入 (D)以上皆是  D
保稅品來源主要有哪三類？ (A)國外進口 (B)保稅區 (C)課稅區需沖退稅而報關者 (D)以上皆是    D
不管東西從哪裡來，我們都一定是用最快的方式安排入廠，所以我估廠商出貨後三天我就能收到貨是可以的，機台入廠後就定位就能開始使用了，機台名牌上的資料就算我是user(使用者)也可以不用理會。    X
舊廠房拆掉之廢水槽出區外處理廠商可以請司機直接載運出區，不用開立放行單。    X
SPEC (SOP) 為_______規範。(A)內部規格書(B)標準作業規範(C)作業流程(D)內部作業流程    B
"以下關於ECN分類說明何者正確？
(A)TECN為緊急變更通知，不得用於規格的變更或主要或重要的變更，除非客戶的同意並有證明文件
(B)EECN為暫時性變更通知，每次最長有效期為8週，版次無須更新
(C)PECN為永久性變更通知，版次須更新
(D)以上皆非"    C
FMEA之Spec 的定期審核年限為_____個月。(A)一年(B)二年(C)三個月(D)六個月  D
Control Plan之Spec 的定期審核年限為_____年。(A)1年(B)半年(C)二年(D)三個月   A
SPC之Spec 的定期審核年限為_____。(A)3個月(B)6個月(C)1年(D)2年   A
ASE SPEC編碼中「廠區別/部門代碼」是編在第2組。  X
ASE SPEC編碼中「文件階層/種類」是編在第1組。    X
ASE SPEC編碼中「製程類別碼」是編在第4組。   X
ASE SPEC編碼中「文件序號」是編在第3組。 X
G8D中「原因分析及証實」為D5。   X
G8D中「永久改善措施標準化/系統性預防建議」為D6。    X
G8D中「暫時性的對策實施及確認」為D4。   X
G8D中「永久改善行動的對策實施效果確認」為D5。   O
"G8D中D0為徵兆 / ___________。
(A)成立改善小組
(B)描述問題
(C)原因分析及証實
(D)緊急反應措施"    D
"G8D 要求要有 Problem Statement(問題說明)，以真實、可計算的數據詳細描述問題，請問5W2H有哪幾項？
(A)Who, What, When, Wherever, Why, However, How Much
(B)Who, What, When, Where, Why, How, How Many
(C)Who, What, Whenever, Where, Why, How, How Much
(D)Who, What, Whenever, Wherever, Why, However, How Many"   B
G8D學習的最終目的為「強調G8D的精神所在」與「利用8個步驟來解決客戶抱怨的永久改善方法」。 O
Issuer會收到系統mail通知「Initiator Working - Check PO complete， Please working」，可開始替客戶服務的IPO 號碼除了有 IPO No.、Rebate No.，還有_______ No.。(請寫英文)   FOC
IPO系統中，各類編碼第一碼(ex: A1204074)的「A」代表______廠？(請寫中文)  封裝
IPO系統中，各類編碼第一碼(ex: T1204074)的「T」代表______廠？(請寫中文)  測試
ASE的品質政策為：提供一流品質，___________。(A)滿足客戶要求 (B)達成客戶期待 (C)超越客戶期望 C
"在商業合約中不常看到以下哪種法律相關條款？
(A)Product Liability(產品責任)與Warranty / Guarantee (保固責任)
(B)IP Non-Infringement (不侵害智慧財產權責任)
(C)Indemnification (賠償條款)
(D)Non-Compete Clause (競業禁止條款)"   D
日月光高雄廠機密資訊等級中，研發項目技術資訊為Confidential C。  X
日月光高雄廠機密資訊等級中，研發項目技術資訊為Confidential D。  X
日月光高雄廠機密資訊等級中，公開發表著作之擷取訊息為Confidential B。    X
日月光高雄廠機密資訊等級中，公開發表著作之擷取訊息為Confidential A。    X
"何者為計量值管制圖的種類？(1)不良率管制圖 / P Chart (2)不良數管制圖 / nP Chart (3)平均值與標準差管制圖/X - Sigma Chart (4)缺點數管制圖 / C Chart (5)平均值與全距管制圖/X - R Chart (6)單位缺點管制圖 / U Chart
(A)1,5
(B)3,4
(C)3,5
(D)2,6" C
魚骨圖中魚頭向右為________型(原因追求)魚骨圖，用來找原因。(A)課題達成 (B)問題解決 (C)目標達成(D)問題分析    B
魚骨圖中魚頭向左為________型(對策擬定)魚骨圖，用來找方法。(A)課題達成 (B)問題解決 (C)目標達成(D)問題分析    A
柏拉圖的用途有：作為降低不良之依據、決定改善之主要目標、確認改善效果與配合特性要因圖使用。  O
"EU RoHS管制的有害物質與其規格值的對應何者正確？
(A)Cd(鎘)，<1000 ppm
(B)Pb(鉛)，<100 ppm
(C)Hg(汞)，<1000 ppm
(D)PBDE(多溴聯苯醚)，<100 ppm"  C
目前，ASE產品的定義可分為Green及Non-green兩種產品，其中ASE Green的產品又可分為Green code R 及Green code ____。(A)G (B)N (C)C (D)W   A
在供應鏈有害物質管理中，ASE通常會要求供應商提供保證書、第三檢驗單位的報告(Test report, SGS report)、MSDS(SDS,物質安全資料表)等GP證明文件。  O
做GP的目標有：限制有害物質的使用；做回收、再利用、再循環；改進生命周期。    O
ASE的"GP"為Green ___________。 (A)Plant (B)Partner (C)Product (D)Process    C
SONY的"GP"為Green ___________。 (A)Partner (B)Product (C)Plant (D)Process   A
ASE有害物質管理系統為IECQ QC_________系統，此系統建構在ISO 9001管理系統上，發展出有害物質管理 (Hazardous Substance Process Management， HSPM) ，同時可滿足 WEEE、RoHS及客戶要求。(A)07000 (B)08000 (C)09000 (D)01000    B
"目前ASE「Flip Chip」 產品哪一個部位含有高含量的鉛(Pb)可以符合Eu RoHS 排外條款？
(A)Underfill
(B)Die
(C)Bumping
(D)Substrate"   C
公司每半年度的績效考核區分為A/B/C/D ，共四個等級。  O
ASE績效考核頻率為每_____實施績效考核一次。(A)一年 (B)二年 (C)半年 (D)三個月 C
SHTC(Strategic High-tech Commodities)為____高科技產品。(A)戰略性 (B)策略性 (C)危險性    A
工程師小明，今天需把 IC sample 由 K7 拿至 K10 做實驗，需開立__________。(A)跨棟攜出單 (B)跨棟放行單 (C)e-shiping    B
在EPA管制內若需使用紙張，則必須要置於靜電袋內並與產品保持30公分以上之距離。 O
ECO-Partner以相信供應商的觀念，ASE 無需做XRF檢驗過程，僅需要求供應商提供測試報告及SDS即可。 X
手持式XRF-970機台基本上分為兩種測試模式 : 塑膠模式和金屬模式。  O
ASE材料標籤分為兩種顏色，綠色材料為白色標籤，非綠色材料為粉紅色標籤。   O
"ECO-Partner 要求 XRF 管制幾項有害物質？
(A)5項
(B)6項
(C)7項
(D)10項"    C
"執行XRF測試時，依ASE產品測試面種類哪一個適合選擇金屬模式？
(A)Compound
(B)Heat spreader
(C)Ball / substrate
(D)Die / substrate" B
"當測試sample面為金屬材料，且XRF選擇金屬模式進行測試時，下列哪一個測試項目不用被測試 ?
(A)Pb(鉛)
(B)Cl(氯)
(C)Hg(汞)
(D)Cr(鎘)"  B
"下列關於「品質管理系統與稽核」的描述，何者為誤？
(A)品質即為產品適用性
(B)下游作業即是客戶
(C)客戶稽核為第一者稽核
(D)品管圈活動希望企業組織由下而上推廣品質的重要性"  C
發現問題時,應該優先改善哪一種問題?(A)提升製程水準 (B)降低異常 (C)以上皆是 (D)以上皆非。 B
常用於原因解析的手法有哪些?(A)FTA (B) QC7 手法 (C) 3*5Why (D)以上皆是。 D
5M1E指的是 人、機、料、法、 、量測。(請填入中文)    環境
發現問題時,應該優先改善哪一種問題?(A)提升製程水準 (B)降低異常 (C)以上皆是 (D)以上皆非。 B
常用於原因解析的手法有哪些?(A)FTA (B) QC7 手法 (C) 3*5Why (D)以上皆是。 D
5M1E指的是人、機、料、法、 、量測。(請填入2個字中文)    環境
5M1E指的是 、機、料、法、環境、量測。(請填入1個字中文)  人
"下列各種智慧財產權，不需要向機關申請核可或註冊登記者有哪些？
1. 營業秘密 2. 專利權 3. 商標權 4. 著作權
(A)1、2 (B)2、3 (C)3、4 (D)1、4"    D
"下列有關智慧財產權風險控制措施之敘述，何者正確？
(A)為了節省時間，研發紀錄可以大概、草略地撰寫即可。
(B)只要工作上有需要，可以任意下載所需要的軟體或程式。
(C)為了提升工作表現，可以使用前雇主的研發技術。
(D)以上皆非。"  D
"若員工不當取得公司營業秘密，並將該秘密洩漏給第三人，所生之法律責任或效果有哪些？
(A)刑事責任，最高可處十年以下有期徒刑，得併科罰金。
(B)民事責任，應負侵權損害之賠償責任。
(C)公司可不經預告終止與勞工之勞動契約關係，並無須支付資遣費與預告工資。
(D)以上皆是。"  D
"送交法律文件予法務單位時之應注意事項，何者為正確？
(A)需給予法務同仁一定之審閱時間，不在簽約之際才提出。
(B)需協助法務同仁了解該事件的背景資訊。
(C)法務提供修改建議後，送審單位應先確認合約內容是否恰當，如有問題應與法務再討論；合約內容待內部確認完成後再提供予對方確認與協商。
(D)以上皆是。"  D
"如有合約審閱或需法務部門協力處理之事務，應以 Notes 郵件寄予哪個信箱？
(A)legal@aseglobal.com
(B)justice@aseglobal.com
(C)law@aseglobal.com
(D)legal@usi.com.tw"    A
"請依序排出合約送審時的正確流程：
1. 申請單位提出文件簽署之需求 2. 文件送審 3. 審查完成 4. 法務及其他權責單位提出審查意見 5. 申請單位確認該交易模式與相關交易條件
(A)1→2→3→4→5
(B)1→4→5→2→3
(C)1→5→2→4→3
(D)5→4→3→2→1"   C
"有關契約審閱及簽署應注意的事項，下列何者為正確?
(A)應先確認簽署文件之目的、必要性，以及我司與相對人的法律關係
(B)確認簽約主體(公司名稱)、簽約代表人是否具有合法授權
(C)確認合約所載之交易條件是否正確
(D)以上皆是"    D
"有關各單位於執行職務時應注意的遵法事項之敘述，何者為正確？
(A)遇有業務上相關法律問題時，應向法務單位諮詢及請求協助。
(B)執行業務時應確實遵循法令。
(C)業務執行前應審慎做好風險評估。
(D)相關法律文件應送交法務部門審閱。
(E)以上皆是。"  E
"下列有關智慧財產權之保護及所衍生之風險控管措施之敘述，何者正確？
(A)揭露資訊前，應確認是否已簽署保密契約。
(B)資訊揭露貫徹 Need-to-Know 原則。
(C)不使用前雇主或其他人之機密運用於工作上。
(D)對於他人揭露予我司的資訊，應採取適當與合理之保密措施。
(E)以上皆是"    E
"下列有關智慧財產權之定義及敘述，何者正確？
(A)一種無體財產權
(B)人類精神活動之成果
(C)能產生財產上之價值
(D)為法律所創設之權利
(E)以上皆是"    E
"下列何者「不」屬於法務部門之職掌與功能？
(A)協助各營運單位解讀相關法令及識別法律風險
(B)因公司營運所生之爭議與訴訟案件處理
(C)提供員工私人法律問題之諮詢
(D)以上皆非"    D
"下列哪些文件應送交法務單位審閱？
(A)合約
(B)和解書
(C)保證函
(D)函覆裁罰性函文
(E)以上皆是"    E
"法務單位之權責業務有哪些？
1. 合約審閱 2. 定期追蹤更新法規 3. 訴訟案件之處理 4. 爭端解決 5. 協助各部門解釋法規
(A)1、2、3、4
(B)1、2、3、5
(C)2、3、4、5
(D)1、2、3、4、5"   D
'''


def clean_text(text: str) -> str:
    if text is None:
        return ""

    replacements = {
        "\u0081": " ",
        "\u0082": " ",
        "\u0083": " ",
        "\u0084": " ",
        "\u00a0": " ",
        "\ufeff": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)

    return text.strip()


def load_questions():
    questions = []

    # 將題庫按照「一題一筆」整理。
    # 有些題目本身跨多行並使用雙引號包住，
    # 所以先把這些多行題目合併起來。
    lines = QUESTION_BANK.splitlines()

    records = []
    buffer = ""
    in_quotes = False

    for line in lines:
        line = line.rstrip()

        if not line.strip():
            continue

        # 如果目前正在處理多行雙引號題目
        if in_quotes:
            buffer += "\n" + line

            # 雙引號數量為偶數，代表題目結束
            if buffer.count('"') % 2 == 0:
                records.append(buffer)
                buffer = ""
                in_quotes = False

            continue

        # 題目以雙引號開始，但這一行尚未結束
        if line.lstrip().startswith('"') and line.count('"') % 2 == 1:
            buffer = line
            in_quotes = True
            continue

        records.append(line)

    # 防止最後還有未處理的資料
    if buffer:
        records.append(buffer)

    for record in records:

        record = record.strip()

        if not record:
            continue

        # 跳過標題
        if record.startswith("題目"):
            continue

        # 將跨行題目的換行變成空格
        record = re.sub(r"\s*\n\s*", " ", record)

        # 移除題目最外層的雙引號
        if (
            len(record) >= 2
            and record.startswith('"')
            and record.endswith('"')
        ):
            record = record[1:-1].strip()

        # 答案永遠在題目最後面，
        # 因此從最後一個空白切開。
        match = re.match(
            r"^(.*?)\s+([A-E]|O|X|FOC|封裝|測試|環境|人)\s*$",
            record,
            re.IGNORECASE
        )

        if not match:
            continue

        question = clean_text(match.group(1))
        answer = clean_text(match.group(2)).upper()

        if not question:
            continue

        if not answer:
            continue

        questions.append(
            {
                "id": len(questions),
                "question": question,
                "answer": answer,
            }
        )

    if not questions:
        messagebox.showerror(
            "題庫錯誤",
            "內建題庫沒有讀到任何題目。"
        )
        sys.exit(1)

    return questions


def load_wrong_ids():
    if not WRONG_FILE.exists():
        return []

    try:
        data = json.loads(
            WRONG_FILE.read_text(
                encoding="utf-8"
            )
        )

        return [
            int(x)
            for x in data
            if str(x).isdigit()
        ]

    except Exception:
        return []


def save_wrong_ids(ids):
    WRONG_FILE.write_text(
        json.dumps(
            sorted(set(ids)),
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


class QuizApp:

    def __init__(self, root):
        self.root = root

        self.root.title(APP_TITLE)
        self.root.geometry("900x720")
        self.root.minsize(760, 620)

        self.questions = load_questions()
        self.wrong_ids = set(load_wrong_ids())

        self.mode = "all"

        self.queue = []

        self.current = None
        self.answered = False

        self.total_answered = 0
        self.correct_count = 0
        self.score = 0

        self.build_ui()

        self.start_all()


    def build_ui(self):

        top = tk.Frame(
            self.root,
            padx=14,
            pady=10
        )

        top.pack(
            fill="x"
        )


        tk.Button(
            top,
            text="隨機50題",
            width=12,
            command=self.start_all
        ).pack(
            side="left",
            padx=4
        )


        tk.Button(
            top,
            text="錯題複習",
            width=12,
            command=self.start_wrong
        ).pack(
            side="left",
            padx=4
        )


        tk.Button(
            top,
            text="清除錯題",
            width=12,
            command=self.clear_wrong
        ).pack(
            side="left",
            padx=4
        )


        self.mode_label = tk.Label(
            top,
            text="",
            anchor="e"
        )

        self.mode_label.pack(
            side="right",
            padx=8
        )


        stat = tk.Frame(
            self.root,
            padx=16,
            pady=4
        )

        stat.pack(
            fill="x"
        )


        self.stat_label = tk.Label(
            stat,
            text="",
            font=(
                "Microsoft JhengHei UI",
                11,
                "bold"
            )
        )

        self.stat_label.pack(
            side="left"
        )


        self.progress_label = tk.Label(
            stat,
            text=""
        )

        self.progress_label.pack(
            side="right"
        )


        line = tk.Frame(
            self.root,
            height=1,
            bd=1,
            relief="sunken"
        )

        line.pack(
            fill="x",
            padx=16,
            pady=(4, 8)
        )


        question_frame = tk.Frame(
            self.root,
            padx=20,
            pady=8
        )

        question_frame.pack(
            fill="both",
            expand=True
        )


        self.question_text = tk.Text(
            question_frame,
            wrap="word",
            font=(
                "Microsoft JhengHei UI",
                15
            ),
            height=15,
            padx=12,
            pady=12,
            state="disabled"
        )

        self.question_text.pack(
            fill="both",
            expand=True
        )


        self.answer_frame = tk.Frame(
            self.root,
            padx=20,
            pady=8
        )

        self.answer_frame.pack(
            fill="x"
        )


        self.result_label = tk.Label(
            self.root,
            text="",
            font=(
                "Microsoft JhengHei UI",
                13,
                "bold"
            ),
            pady=6
        )

        self.result_label.pack(
            fill="x"
        )


        bottom = tk.Frame(
            self.root,
            padx=20,
            pady=12
        )

        bottom.pack(
            fill="x"
        )


        self.next_button = tk.Button(
            bottom,
            text="下一題",
            width=14,
            command=self.next_question,
            state="disabled"
        )

        self.next_button.pack(
            side="right"
        )


        tk.Label(
            bottom,
            text="快捷鍵：O / X / A~E 可直接作答；Enter 可送出填充題。",
            anchor="w"
        ).pack(
            side="left"
        )


        for key in [
            "o",
            "x",
            "a",
            "b",
            "c",
            "d",
            "e"
        ]:

            self.root.bind(
                key,
                self.keyboard_answer
            )

            self.root.bind(
                key.upper(),
                self.keyboard_answer
            )


    def set_question_text(self, text):

        self.question_text.config(
            state="normal"
        )

        self.question_text.delete(
            "1.0",
            "end"
        )

        self.question_text.insert(
            "1.0",
            text
        )

        self.question_text.config(
            state="disabled"
        )


    def start_all(self):

        self.mode = "all"

        question_count = min(
            QUESTIONS_PER_ROUND,
            len(self.questions)
        )

        # 每次從完整題庫隨機抽 50 題
        # random.sample 不會在同一輪抽到重複題目
        self.queue = random.sample(
            range(len(self.questions)),
            question_count
        )

        self.reset_session_stats()

        self.next_question()


    def start_wrong(self):

        valid_wrong_questions = [
            question_id
            for question_id in self.wrong_ids
            if 0 <= question_id < len(self.questions)
        ]

        if not valid_wrong_questions:

            messagebox.showinfo(
                "錯題複習",
                "目前沒有錯題，先去刷題吧！"
            )

            return


        self.mode = "wrong"

        self.queue = valid_wrong_questions[:]

        random.shuffle(
            self.queue
        )

        self.reset_session_stats()

        self.next_question()


    def reset_session_stats(self):

        self.total_answered = 0
        self.correct_count = 0
        self.score = 0

        self.update_stats()


    def clear_wrong(self):

        if not self.wrong_ids:

            messagebox.showinfo(
                "清除錯題",
                "目前沒有錯題。"
            )

            return


        confirm = messagebox.askyesno(
            "清除錯題",
            "確定要清除全部錯題紀錄嗎？"
        )


        if confirm:

            self.wrong_ids.clear()

            save_wrong_ids(
                self.wrong_ids
            )

            self.update_stats()


            if self.mode == "wrong":

                self.start_all()


    def next_question(self):

        # queue 空掉代表這一輪做完
        if not self.queue:

            if self.mode == "wrong":

                self.finish_wrong_review()

                return

            else:

                self.finish_exam()

                return


        question_id = self.queue.pop(0)

        self.current = self.questions[
            question_id
        ]

        self.answered = False


        self.next_button.config(
            state="disabled"
        )


        self.result_label.config(
            text=""
        )


        self.clear_answer_frame()


        self.set_question_text(
            self.current["question"]
        )


        self.render_answer_controls()


        self.update_stats()


    def finish_exam(self):

        wrong_count = (
            self.total_answered
            -
            self.correct_count
        )


        final_score = (
            self.correct_count
            *
            SCORE_PER_CORRECT
        )


        if self.total_answered == 0:

            rate = 0

        else:

            rate = (
                self.correct_count
                /
                self.total_answered
                *
                100
            )


        if final_score >= 90:

            level = "優秀"

        elif final_score >= 80:

            level = "良好"

        elif final_score >= 70:

            level = "不錯"

        elif final_score >= 60:

            level = "及格"

        else:

            level = "需要加強"


        messagebox.showinfo(
            "本輪測驗完成",
            (
                f"50 題測驗完成！\n\n"
                f"答對：{self.correct_count} 題\n"
                f"答錯：{wrong_count} 題\n\n"
                f"總分：{final_score} / 100\n"
                f"正確率：{rate:.0f}%\n"
                f"評價：{level}\n\n"
                f"目前錯題庫："
                f"{len(self.wrong_ids)} 題"
            )
        )


        again = messagebox.askyesno(
            "再考一次",
            "要重新隨機抽 50 題嗎？"
        )


        if again:

            self.start_all()

        else:

            self.mode_label.config(
                text=(
                    "本輪完成"
                    f" ｜ 錯題庫："
                    f"{len(self.wrong_ids)} 題"
                )
            )


    def finish_wrong_review(self):

        remaining = [
            question_id
            for question_id in self.wrong_ids
            if 0 <= question_id < len(self.questions)
        ]


        if not remaining:

            messagebox.showinfo(
                "錯題複習完成",
                (
                    "太好了！\n\n"
                    "目前錯題已經全部答對。"
                )
            )

            self.start_all()

            return


        again = messagebox.askyesno(
            "錯題複習完成",
            (
                f"這輪錯題已做完。\n\n"
                f"目前還有 {len(remaining)} 題錯題。\n\n"
                f"要繼續複習嗎？"
            )
        )


        if again:

            self.queue = remaining[:]

            random.shuffle(
                self.queue
            )

            self.reset_session_stats()

            self.next_question()

        else:

            self.start_all()


    def clear_answer_frame(self):

        for widget in self.answer_frame.winfo_children():

            widget.destroy()


    def render_answer_controls(self):

        answer = self.current["answer"]


        # O / X 題
        if answer in {
            "O",
            "X"
        }:

            tk.Button(
                self.answer_frame,
                text="O",
                width=12,
                height=2,
                font=(
                    "Microsoft JhengHei UI",
                    13,
                    "bold"
                ),
                command=lambda: self.submit_answer("O")
            ).pack(
                side="left",
                padx=8
            )


            tk.Button(
                self.answer_frame,
                text="X",
                width=12,
                height=2,
                font=(
                    "Microsoft JhengHei UI",
                    13,
                    "bold"
                ),
                command=lambda: self.submit_answer("X")
            ).pack(
                side="left",
                padx=8
            )

            return


        # 選擇題
        if answer in {
            "A",
            "B",
            "C",
            "D",
            "E"
        }:

            labels = re.findall(
                r"\(([A-E])\)",
                self.current["question"].upper()
            )


            options = []


            for letter in [
                "A",
                "B",
                "C",
                "D",
                "E"
            ]:

                if (
                    letter in labels
                    or
                    letter == answer
                ):

                    options.append(
                        letter
                    )


            # 如果題目格式無法辨識
            # 預設顯示 A~D
            if len(options) <= 1:

                options = [
                    "A",
                    "B",
                    "C",
                    "D"
                ]


                if answer == "E":

                    options.append(
                        "E"
                    )


            for letter in options:

                tk.Button(
                    self.answer_frame,
                    text=letter,
                    width=9,
                    height=2,
                    font=(
                        "Microsoft JhengHei UI",
                        12,
                        "bold"
                    ),
                    command=lambda value=letter:
                        self.submit_answer(value)
                ).pack(
                    side="left",
                    padx=6
                )

            return


        # 填充題
        tk.Label(
            self.answer_frame,
            text="請輸入答案：",
            font=(
                "Microsoft JhengHei UI",
                11
            )
        ).pack(
            side="left"
        )


        self.entry = tk.Entry(
            self.answer_frame,
            font=(
                "Microsoft JhengHei UI",
                13
            ),
            width=24
        )


        self.entry.pack(
            side="left",
            padx=8
        )


        self.entry.focus_set()


        self.entry.bind(
            "<Return>",
            lambda event:
                self.submit_text_answer()
        )


        tk.Button(
            self.answer_frame,
            text="送出",
            width=10,
            command=self.submit_text_answer
        ).pack(
            side="left",
            padx=6
        )


    def keyboard_answer(self, event):

        if self.answered:

            return


        if not self.current:

            return


        key = event.keysym.upper()


        valid_keys = {
            "O",
            "X",
            "A",
            "B",
            "C",
            "D",
            "E"
        }


        if key not in valid_keys:

            return


        answer = self.current["answer"]


        if answer in valid_keys:

            self.submit_answer(
                key
            )


    def submit_text_answer(self):

        if self.answered:

            return


        value = clean_text(
            self.entry.get()
        )


        if not value:

            return


        self.submit_answer(
            value
        )


    def submit_answer(self, user_answer):

        if self.answered:

            return


        if not self.current:

            return


        self.answered = True


        correct_answer = (
            self.current["answer"]
        )


        user_answer = clean_text(
            str(user_answer)
        ).upper()


        self.total_answered += 1


        if user_answer == correct_answer:

            self.correct_count += 1

            self.score += (
                SCORE_PER_CORRECT
            )


            self.result_label.config(
                text=(
                    f"✓ 答對了 "
                    f"+{SCORE_PER_CORRECT} 分"
                )
            )


            # 如果這題原本在錯題庫
            # 答對後移除
            self.wrong_ids.discard(
                self.current["id"]
            )


        else:

            self.result_label.config(
                text=(
                    f"✗ 答錯了 "
                    f"正確答案："
                    f"{correct_answer}"
                )
            )


            # 答錯加入錯題庫
            self.wrong_ids.add(
                self.current["id"]
            )


        save_wrong_ids(
            self.wrong_ids
        )


        self.disable_answer_controls()


        self.next_button.config(
            state="normal"
        )


        self.update_stats()


    def disable_answer_controls(self):

        for widget in self.answer_frame.winfo_children():

            try:

                widget.config(
                    state="disabled"
                )

            except tk.TclError:

                pass


    def update_stats(self):

        if self.mode == "wrong":

            mode_text = "錯題複習"

        else:

            mode_text = "隨機50題"


        self.mode_label.config(
            text=(
                f"模式：{mode_text}"
                f" ｜ "
                f"錯題庫："
                f"{len(self.wrong_ids)} 題"
            )
        )


        if self.total_answered == 0:

            rate = 0

        else:

            rate = (
                self.correct_count
                /
                self.total_answered
                *
                100
            )


        if self.mode == "all":

            current_score = (
                self.correct_count
                *
                SCORE_PER_CORRECT
            )

            self.stat_label.config(
                text=(
                    f"答對："
                    f"{self.correct_count}"
                    f" / "
                    f"{self.total_answered}"
                    f" ｜ "
                    f"目前分數："
                    f"{current_score}"
                    f" / 100"
                    f" ｜ "
                    f"正確率："
                    f"{rate:.0f}%"
                )
            )

        else:

            self.stat_label.config(
                text=(
                    f"錯題複習："
                    f"{self.correct_count}"
                    f" / "
                    f"{self.total_answered}"
                    f" ｜ "
                    f"正確率："
                    f"{rate:.0f}%"
                )
            )


        if self.mode == "all":

            current_number = (
                self.total_answered
                +
                1
            )


            if current_number > QUESTIONS_PER_ROUND:

                current_number = (
                    QUESTIONS_PER_ROUND
                )


            self.progress_label.config(
                text=(
                    f"第 {current_number}"
                    f" / "
                    f"{QUESTIONS_PER_ROUND} 題"
                )
            )

        else:

            self.progress_label.config(
                text=(
                    f"剩餘錯題："
                    f"{len(self.queue)} 題"
                )
            )


def main():

    root = tk.Tk()

    QuizApp(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()