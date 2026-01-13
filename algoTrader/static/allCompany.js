// === DATA SETUP ===
function waitForElement(selector, {root = document, timeout = 5000} = {}) {
  return new Promise((resolve, reject) => {
    const el = root.querySelector(selector);
    if (el) return resolve(el);

    const obs = new MutationObserver((mutations, observer) => {
      const found = root.querySelector(selector);
      if (found) {
        observer.disconnect();
        clearTimeout(timer);
        resolve(found);
      }
    });

    obs.observe(root, { childList: true, subtree: true });

    const timer = setTimeout(() => {
      obs.disconnect();
      reject(new Error('timeout waiting for ' + selector));
    }, timeout);
  });
}

document.addEventListener("DOMContentLoaded", function () {
const CompaniesLtp=document.getElementById("Companies_LTP");
CompaniesLtp.addEventListener('click',async function(){
  cleanupAll();
mainDiv=document.getElementById("form-container");

mainDiv.innerHTML="";
mainDiv.innerHTML=`
<div class="all_company_container">
            <div class="market-container">
                <h1>Market Watch</h1>
                <div class="company-list" id="companyList"></div>
            </div>
            <div class="graph-container">
                <div id="companyInfoArea">
                    <div class="chart-title">
                        <div class="comp_data1">
                            <div class="comp_name1" id="companyName">Company Name</div>
                            <div class="comp_name1"> 
                                <div class="comp_name2" id="companyPrice">&#8377;11,000</div>
                                <div class="price_data">
                                    <div id="priceChange">price change</div>
                                    <div id="percentChange">percent change</div>
                                </div>
                            </div>
                        </div>
                        <div class="comp_data">
                            <div class="comp_name" id="highPrice">1D high: &#8377;5500</div>
                            <div class="comp_name" id="lowPrice">1D low: &#8377;5440</div>  
                        </div>
                    </div>  
                    <div class="chart-half-width">
                        <div id="chart" class="chart-container"></div>
                    </div>
                </div>
                <div class="bottom-spacer"> </div>
            </div>
  </div>`;
    
const REAL_COMPANY_NAMES= ['Shaily Engineering Plastics Ltd', 'Aditya Birla Fashion & Retail Ltd', 'AAVAS Financiers Ltd',
     'ACME Solar Holdings Ltd ', 'Aadhar Housing Finance Ltd', 'Aarti Industries Ltd', 'Acutaas Chemicals Ltd',
      'Aditya Birla Lifestyle Brands Ltd', 'Aegis Vopak Terminals Ltd', 'Afcons Infrastructure Ltd',
       'Affle 3i Ltd', 'Akzo Nobel India Ltd', 'Alembic Pharmaceuticals Ltd ', 'Alkem Laboratories Ltd',
        'Apollo Tyres Ltd', 'Asahi India Glass Ltd ', 'Ashok Leyland Ltd', 'Astra Microwave Products Ltd ',
         'Astral Ltd', 'Astrazeneca Pharma India Ltd ', 'Ather Energy Ltd', 'Atul Ltd', 'Aurobindo Pharma Ltd ',
          'Avenue Supermarts Ltd ', 'BASF India Ltd ', 'BEML Ltd', 'BLS International Services Ltd ', 'BSE Ltd ',
           'Belrise Industries Ltd ', 'Bharat Electronics Ltd ', 'Bharat Heavy Electronics Ltd ', 
           'Bharti Airtel Ltd ', 'Bharti Hexacom Ltd ', 'Biocon Ltd', 'Blue Jet Healthcare Ltd', 'Blue Star Ltd',
            'Brookfield India Real Estate Trust', 'CEAT Ltd ', 'CESC Ltd', 'CG Power & Industrial Solutions Ltd',
            'Capri Global Capital Ltd ', 'Choice International Ltd', 'Cholamandalam Investment & Finance Company  Ltd',
             'Clean Science & Technology Ltd ', 'Coforge Ltd', 'Computer Age Management Services Ltd', 'Concord Biotech Ltd',
              'Credit Access Grameen Ltd ', 'Cummins India Ltd', 'DCM Shriram Ltd', 'Dabur India Ltd ', 'Deepak Fertilisers & Petrochemicals Corp Ltd',
               'Delhivery Ltd', 'Divis Laboratories Ltd', 'Dixon Technologies (India) Ltd ', 'Dr Agarwals Health Care Ltd', 'EID Parry (India) Ltd',
                'EIH Ltd', 'ERIS Lifesciences Ltd', 'Embassy Developments Ltd', 'Embassy Office Parks REIT', 'Emcure Pharmaceuticals Ltd', 'Eureka Forbes Ltd',
                 'Finolex Industries Ltd', 'Five-Star Business Finance Ltd', 'GE Vernova T&D India Ltd', 'GMR Airports Ltd', 
                 'Gland Pharma Ltd', 'Glaxosmithkline Pharmaceuticals Ltd', 'Godawari Power & Ispat Ltd', 'Godrej Consumer Products Ltd',
                  'Godrej Industries Ltd', 'Grindwell Norton Ltd', 'Gujarat Fluorochemicals Ltd', 'Gujarat State Petronet Ltd',
                   'HBL Engineering Ltd', 'HDFC Asset Management Company Ltd', 'HFCL Ltd', 'Havells India Ltd', 'Home First Finance Company India Ltd', 
                   'Honeywell Automation India Ltd', 'ITD Cementation India Ltd', 'IndiGrid Infrastructure Trust', 'Indiamart Intermesh Ltd', 
                   'Indian Renewable Energy Development Agency Ltd', 'Indraprastha Gas Ltd', 'Indus Towers Ltd', 'Inox India Ltd',
                    'Inox Wind Ltd', 'Intellect Design Arena Ltd', 'Ipca Laboratories Ltd', 'Ircon International Ltd', 'J B Chemicals & Pharmaceuticals Ltd', 
                    'JBM Auto Ltd', 'JM Financial Ltd', 'Jindal Stainless Ltd ', 'Jubilant Ingrevia Ltd', 'Jubilant Pharmova Ltd', 
                    'K E C International Ltd ', ' K P R  Mill Ltd', 'KEI Industries Ltd ', 'KPI Green Energy Ltd', 'KSB Ltd', 
                    'Kalpataru Projects International Ltd ', ' Kalyan Jewellers India Ltd', 'Kaynes Technology India Ltd',
                     'Kirloskar Oil Engines Ltd', 'L & T Finance Ltd', 'Lemon Tree Hotels Ltd ', 'Lupin Ltd ', 
                     'Mahindra & Mahindra Financial Services Ltd ', 'Mahindra & Mahindra Ltd', 'Manappuram Finance Ltd ',
                      'Mankind Pharma Ltd', 'Maruti Suzuki India Ltd', 'Metro Brands Ltd ', 'Metropolis healthcare Ltd ',
                       'Mindspace Business Parks REIT', 'Multi Commodity Exchange of India Ltd ', 'Muthoot Finance Ltd',
                        'Natco Pharma Ltd', ' Navin Fluorine International Ltd', 'Netweb Technologies India Ltd',
                         'Neuland Laboratories Ltd ', 'Nexus Select Trust', 'Nippon Life India Asset Management Ltd', 
                         'Nuvama Wealth Management Ltd', 'Olectra Greentech Ltd', 'One 97 Communications Ltd ',
                          'OneSource Specialty Pharma Ltd', 'Oswal Pumps Ltd', 'PB Fintech Ltd', 'PG Electroplast Ltd',
                           'PTC Industries Ltd', 'PVR Inox Ltd', 'Paradeep Phosphates Ltd', 'Persistent Systems Ltd', 
                           'Phoenix Mills Ltd', 'Pidilite Industries Ltd', 'Piramal Pharma Ltd', 'Poly Medicure Ltd',
                            'Polycab India Ltd', 'Poonawalla Fincorp Ltd', 'Prestige Estates Projects Ltd ', 'Privi Speciality Chemicals Ltd',
                             'Procter & Gamble Health Ltd', 'Prudent Corporate Advisory Services Ltd', 'R R Kabel Ltd', 'Redington Ltd',
                              'SJVN Ltd', 'SRF Ltd ', 'Sagility India Ltd', 'Sai Life Sciences Ltd', 'Saregama India Ltd',
                               'Schneider Electric Infrastructure Ltd', 'Shriram Pistons & Rings Ltd', 'Siemens Energy India Ltd', 
                               'Solar Industries India Ltd ', 'Sona BLW Precision Forgings Ltd ', 'Star Health & Allied Insurance Company Ltd',
                                'Sumitomo Chemical India Ltd', 'Sun Pharmaceutical Industries Ltd ', 'Sundaram Finance Ltd',
                                 'Sundram Fasteners Ltd', 'Supreme Industries Ltd', 'Suzlon Energy Ltd', 'Swan Energy Ltd', 'Syrma SGS Technology Ltd',
                                  'TVS Motor Company Ltd', 'Tata Communications Ltd', 'Techno Electric & Engineering Company Ltd', 'Tega Industries Ltd', 'Thermax Ltd',
                                   'Tilaknagar Industries Ltd', 'Timken India Ltd', 'Titagarh Rail Systems Ltd', 'Titan Company Ltd', 
                                   'Torrent Pharmaceuticals Ltd', 'UPL Ltd', 'Uno Minda Ltd', 'Usha Martin Ltd', 'V-Guard Industries Ltd',
                                    'Ventive Hospitality Ltd', 'Vishal Mega Mart Ltd', 'Vodafone Idea Ltd', 'Waaree Renewable Technologies',
                                     'Wockhardt Ltd ', 'Zee Entertainment Enterprises Ltd', 'Zen Technologies Ltd', 'Zinka Logistics Solutions Ltd',
                                      'Zydus Lifesciences Ltd', 'Aditya Birla Fashion & Retail Ltd', 'Aarti Drugs Ltd', 'Apollo Micro Systems Ltd', 
                                      'Arvind Fashions Ltd', 'Avalon Technologies Ltd', 'Borosil Renewables Ltd', 'Cigniti Technologies Ltd',
                                       'Crizac Ltd', 'Datamatics Global Services Ltd', 'Ellenbarrie Industrial Gases Ltd', 'Enviro Infra Engineers Ltd',
                                        'Fedbank Financial Services Ltd', 'Fiem Industries Ltd', 'Gujarat Alkalies & Chemicals Ltd', 
                                        'Gujarat  Themis Biosyn Ltd', 'IFB Industries Ltd', 'Innova Captab Ltd', 'Jana Small Finance Bank Ltd',
                                         'KRN Heat Exchanger and Refrigeration Ltd', 'Karnataka Bank Ltd', 'Kaveri Seed Company Ltd', 'Kingfa Science & Technology (India) Ltd',
                                          'MAS Financial Services Ltd', 'Network People Services Technologies Ltd', 'Orient Electric Ltd', 'Paras Defence and Space Technologies Ltd',
                                           'Pricol Ltd', 'Purvankara Ltd', 'Quality Power Electrical Equipments Ltd', 'R Systems International Ltd ',
                                            'Rallis India Ltd', 'S J S Enterprises Ltd', 'SIS Ltd', 'SML ISUZU Ltd', 'Sanathan Textiles Ltd',
                                             'Sheela Foam Ltd', 'Smartworks Coworking Spaces Ltd', 'Subros Ltd', 'Tamilnad Mercantile Bank Ltd', 
                                             'Texmaco Rail  & Engineering Ltd', 'V I P Industries Ltd', 'V2 Retail Ltd', 'Websol Energy System Ltd',
                                              'Yatharth Hospital & Trauma Care Services Ltd', 'Zaggle Prepaid Ocean Services Ltd', '360 One Wam Ltd',
                                               '3M India Ltd', 'ABB India Ltd', 'ACC Ltd', 'APL Apollo Tubes Ltd', 'AU Small Finance Bank Ltd', 
                                               'Abbott India Ltd', 'Adani Energy  Solutions Ltd', 'Adani Enterprises Ltd', 'Adani Green  Energy Ltd ',
                                                'Adani Ports & Special Economic Zone Ltd', 'Adani Power Ltd', 'Adani Total Gas Ltd', 
                                                'Aditya Birla Capital Ltd', 'Ambuja Cements Ltd', 'Anthem Biosciences Ltd', 'Apollo Hospitals Enterprise Ltd',
                                                 'Aptus Value Housing Finance India Ltd', 'Asian Paints Ltd', 'Axis Bank Ltd', 'Bajaj Auto Ltd',
                                                  'Bajaj Finserv Ltd', 'Bajaj Finance Ltd', 'Bajaj Holdings & Investment Ltd', 'Bajaj Housing Finance Ltd',
        'Balkrishna Industries Ltd', 'Bandhan Bank Ltd', 'Bank of Baroda', 'Bank of Maharashtra ', 'Bayer CropScience Ltd', 'Berger Paints India Ltd', 'Bharat Dynamics Ltd',
        'Bharat Forge Ltd', 'Bharat Petroleum Corporation Ltd', 'Bharti Airtel Ltd Partly  Paidup', 'Bosch Ltd', 'Brainbees Solutions Ltd', 'Britannia Industries Ltd',
        'CRISIL Ltd', 'Canara Bank', 'Caplin Point Laboratories Ltd', 'Carborundum Universal Ltd', 'Cholamandalam Financial Holdings Ltd', 'City Union Bank Ltd', 'Coal India Ltd',
        'Cochin Shipyard Ltd', 'Colgate-Palmolive (India) Ltd', 'Container Corporation Of India Ltd', 'Coromandel International Ltd', 'Crompton Greaves Consumer Electricals Ltd', 'DLF Ltd',
        'Dalmia Bharat Ltd', 'Eicher Motors Ltd', 'Endurance Technologies Ltd', 'Escorts Kubota Ltd', 'Eternal Ltd', 'Federal Bank Ltd', 'Fertilizers & Chemicals Travancore Ltd', 'Force Motors Ltd',
        'Fortis Healthcare Ltd', 'GAIL (India) Ltd', 'Gallantt Ispat Ltd', 'General Insurance Corporation of India', 'Glenmark Pharmaceuticals Ltd', 'Global Health Ltd', 'Go Digit General Insurance Ltd',
        'Godfrey Phillips India Ltd', 'Godrej Properties Ltd', 'Grasim Industries Ltd', 'HCL Technologies Ltd', 'HDB Financial Services Ltd', 'HDFC Life Insurance Company Ltd', 'Hero MotoCorp Ltd',
        'hexaware Technologies Ltd', 'Hindalco Industries Ltd', 'Hindustan Aeronautics Ltd', 'Hindustan Petroleum Corporation Ltd', 'Hindustan Unilever Ltd', 'Hindustan Zinc Ltd', 'Hitachi Energy India Ltd',
        'Housing & Urban Development Corporation Ltd', 'Hyundai Motor India Ltd', 'ICICI Bank Ltd', 'ICICI Lombard General Insurance Company Ltd', 'ICICI Prudential Life Insurance Company Ltd', 'IDBI Bank Ltd',
        'IDFC First Bank Ltd', 'IFCI Ltd', 'ITC Hotels Ltd', 'ITC Ltd', 'Indian Bank', 'Indian Hotels Co Ltd', 'Indian Oil Corporation Ltd', 'Indian Overseas Bank', 'Indian Railway Catering & Tourism Corporation Ltd',
        'Indian Railway Finance Corporation Ltd', 'IndusInd Bank Ltd', 'Info Edge (India) Ltd', 'Infosys Ltd', 'Interglobe Aviation Ltd', 'Inventurus Knowledge Solutions Ltd', 'J K Cements Ltd', 'JSW Energy  Ltd', 'JSW Infrastructure Ltd',
        'JSW Steel Ltd', 'Jindal Steel & Services Ltd', 'Jio Financial Services Ltd', 'Jubilant Foodworks Ltd', 'KIOCL Ltd', 'Kansai Nerolac Paints Ltd', 'Kirloskar Brothers Ltd', 'Kotak Mahindra Bank Ltd', 'L T Foods Ltd',
        'L&T Technology Services Ltd', 'LIC Housing Finance Ltd', 'LMW Ltd', 'LTIMindtree Ltd', 'Larsen & Toubro Ltd', 'Laurus Labs Ltd', 'Life Insurance Corporation of India', 'Linde India Ltd', 'Lloyds Metals & Energy Ltd',
        'Lodha Developers Ltd', 'MRF Ltd', 'Mangalore Refinery  And  Petrochemicals Ltd', 'Marico Ltd', 'Max Financial Services Ltd', 'Max Healthcare Institute Ltd', 'Mazagon Dock Shipbuilders Ltd', 'Motherson Sumi Wiring India Ltd',
        'Motilal Oswal Financial Services Ltd', 'Mphasis Ltd', 'NHPC Ltd', 'NMDC Ltd', 'NTPC Green Energy Ltd', 'NTPC Ltd', 'Narayana Hrudayalaya Ltd', 'National Aluminium Company Ltd', 'Nestle India Ltd', 'Nuvoco Vistas Corporation Ltd', 
        'Oberoi Realty Ltd', 'Oil & Natural Gas Corpn Ltd', 'Oil India Ltd', 'Ola Electric Mobility Ltd', 'Oracle Financial Services Software Ltd', 'P I Industries Ltd', 'Page Industries Ltd', 'Patanjali Foods Ltd', 'Petronet LNG Ltd', 
        'Power Finance Corporation Ltd', 'Power Grid Corporation of India Ltd', 'Premier Energies Ltd', 'Procter & Gamble Hygiene and Health Care Ltd', 'Punjab National Bank', 'REC Ltd', 'Radico Khaitan Ltd', 'Rail Vikas Nigam Ltd', 
        'Reliance Industries Ltd', 'Rites Ltd', 'SBI Cards & Payment Services Ltd', 'SBI Life Insurance Company Ltd', 'Samvardhana Motherson International Ltd', 'Schaeffler India Ltd', 'Shree Cement Ltd', 'Shriram Finance Ltd', 'Siemens Ltd', 
        'Sobha Ltd', 'State Bank of India Ltd', 'Steel Authority of India Ltd', 'Supreme Petrochem Ltd', 'Swiggy Ltd', 'Tata Consultancy Services Ltd', 'Tata Consumer Products Ltd', 'Tata Elxsi Ltd', 'Tata Investment Corporation Ltd', 'Tata Motors Ltd', 
        'Tata Power Company Ltd', 'Tata Steel Ltd', 'Tech Mahindra Ltd', 'The Ramco Cements Ltd', 'Torrent Power Ltd', 'Trent Ltd', 'Tube Investments of India Ltd', 'UCO Bank', 'UltraTech Cement Ltd', 'Union Bank of India', 'United Breweries Ltd', 
        'United Spirits Ltd', 'Varun Beverages Ltd', 'Vedanta Ltd', 'Voltas Ltd', 'Waaree Energies Ltd', 'Wipro Ltd', 'Yes Bank Ltd', 'Zensar Technologies Ltd', 'eClerx Services Ltd', '63 Moons Technologies Ltd', 'AIA Engineering Ltd', 'AWL Agri Business Ltd', 
        'Aditya Birla Real Estate Ltd', 'Aditya Birla Sun Life AMC Ltd', 'Aditya Vision Ltd', 'Aegis Logistics Ltd', 'Ajanta Pharma Ltd', 'Allied Blenders & Distillers Ltd', 'Amara Raja Energy & Mobility Ltd', 'Anand Rathi  Wealth Ltd', 'Anant Raj Ltd', 
        'Angel One Ltd', 'Anupam Rasayan India Ltd', 'Apar Industries Ltd', 'Arvind Ltd', 'Ashapura Minechem Ltd', 'Aster DM Healthcare Ltd', 'Bajaj Electricals', 'Balaji Amines Ltd', 'Bata India Ltd', 'Bharat Rasayan Ltd', 'Bikaji Foods International Ltd', 
        'Birlasoft Ltd', 'Bluestone Jewellery & Lifestyle Ltd', 'Blue Dart Express Ltd', 'Bombay Burmah Trading Corporation Ltd', 'Brigade Enterprises Ltd', 'CCL Products (India) Ltd', 'CIE  Automotive India Ltd', 'CMS Info Systems Ltd', 'CSB Bank Ltd', 
        'Can Fin Homes Ltd', 'Cartrade Tech Ltd', 'Castrol India Ltd', 'Central Bank of India', 'Centum Electronics Ltd', 'Century Plyboards (India) Ltd', 'Chalet Hotels Ltd', 'Chambal Fertilisers & Chemicals Ltd', 
        'Cohance Lifesciences Ltd', 'Craftsman Automation Ltd', 'Cyient Ltd', 'Data Patterns (India) Ltd', 'Deepak Nitrite Ltd', 'Devyani International Ltd', 
        'Dilip Buildcon Ltd', 'Doms Industries Ltd', 'Dr Lal Pathlabs Ltd', 'Elecon Engineering Company Ltd', 'Electrosteel Castings Ltd', 'Elgi Equipments Ltd', 
        'Emami Ltd', 'Engineers India Ltd', 'Epigral Ltd', 'Exide Industries Ltd', 'Fine Organic Industries Ltd', 'Finolex Cables Ltd', 'Firstsource Solutions Ltd', 'G R Infraprojects Ltd', 'GHCL Ltd', 'Gabriel India Ltd', 
        'Garden Reach Shipbuilders & Engineers Ltd', 'Gillette India Ltd', 'Godrej Agrovet Ltd', 'Gokaldas Exports Ltd', 'Goldiam International Ltd', 'Gravita India Ltd', 'Great Eastern Shipping Company Ltd', 'Greaves Cotton Ltd', 
        'Gujarat Ambuja Exports Ltd', 'Gujarat Gas Ltd', 'Gujarat Mineral Development Corporation Ltd', 'Hatsun Agro Products Ltd', 'Himadri Speciality Chemical Ltd', 'Hindustan Copper Ltd', 'IIFL Capital Services Ltd', 'IIFL Finance Ltd', 
        'IRB Infrastructure Developers Ltd', 'ISGEC Heavy Engineering Ltd', 'ITI Ltd', 'Indegene Ltd', 'India Cements Ltd', 'Indian Energy Exchange Ltd', 'Indraprastha Medical Corporation Ltd', 'International Gemmological Institude (India) Ltd', 
        'Ion Exchange (India) Ltd', 'J Kumar Infraprojects Ltd', 'JK Lakshmi Cement Ltd', 'JK Paper ltd', 'JSW Holdings Ltd', 'Jaiprakash Power Ventures Ltd', 'Jammu and Kashmir Bank Ltd', 'Jayaswal Neco Industries  Ltd', 'Jindal Saw Ltd', 
        'Jupiter Wagons Ltd', 'Jyothi Labs Ltd', 'Jyoti CNC Automation Ltd', 'KFin Technologies Ltd', 'KNR Constructions Ltd', 'KPIT Technologies Ltd', 'Kajaria Ceramics Ltd', 'Kalpataru Ltd', 'Krishna Institute of Medical Sciences Ltd', 'L G Balakrishnan & Bros Ltd', 
        'Lloyds Enterprises Ltd', 'Magellanic Cloud Ltd', 'Mahanagar Gas Ltd', 'Maharashtra Scooters Ltd', 'Man Infraconstruction Ltd', 'NBCC (India) Ltd', 'NCC Ltd', 'NLC India Ltd', 'Nava Ltd', 'Nazara Technologies Ltd', 'New India Assurance Company Ltd', 
        'Newgen Software Technologies Ltd', 'Niva Bupa Health Insurance Company Ltd', 'Optiemus Infracom Ltd', 'Orient Cement Ltd', 'PCBL Chemical Ltd', 'PNB Housing Finance Ltd', 'PTC India Ltd', 'Pfizer Ltd', 'Praj Industries Ltd', 'Prime Focus Ltd', 'RBL Bank Ltd', 
        'RHI Magnesita India Ltd', 'Railtel Corporation of India Ltd', 'Rain Industries  Ltd', 'Rainbow Childrens Medicare Ltd', 'Rajesh Exports Ltd', 'Ratnamani Metals & Tubes Ltd', 'RattanIndia Enterprises Ltd', 'Raymond Lifestyle Ltd', 'Raymond Ltd', 'Raymond Realty Ltd', 'Responsive Industries Ltd', 'Route Mobile Ltd', 'SBFC Finance Ltd', 'SKF India Ltd', 'Samhi Hotels Ltd', 'Sandur Manganese & Iron Ores Ltd', 'Sanofi Consumer Healthcare India Ltd', 'Sanofi India Ltd', ' Sansera Engineering Ltd', 'Sarda Energy & Minerals Ltd', 'Schloss Bangalore Ltd', 'Senco Gold Ltd', 'Shanthi Gears Ltd', 'Sharda Motor Industries Ltd', 'Shree Renuka Sugars Ltd', 'Shyam Metalics & Energy Ltd', 'Skipper Ltd', 'Sky Gold & Diamonds Ltd', 'Star Cement Ltd', 'Sterlite Technologies Ltd', 'Sun TV Network Ltd', 'Sundaram Finance Holdings Ltd', 'Sunflag Iron & Steel Company Ltd', 'Syngene International Ltd', 'TARC Ltd', 'TBO Tek Ltd', 'TVS Holdings Ltd', 'Tata Chemicals Ltd', 'Tata Technologies Ltd', 'Technocraft Industries (India) Ltd', 'Thyrocare Technologies Ltd', 'Tips Music Ltd', 'Transformers & Rectifiers India Ltd', 'Transrail Lighting Ltd', 'Travel Food Services Ltd', 'Trident Ltd', 'Triveni Turbine Ltd', 
        'UTI Asset Management Company Ltd', 'VST Industries Ltd', 'Va Tech Wabag Ltd', 'Vardhman Textiles  Ltd', 'Vedant Fashions Ltd', 'Vinati Organics Ltd', 'Welspun Corp Ltd', 'Westlife Foodworld Ltd', 'Whirlpool of India Ltd', 'ZF Commercial Vehicle Control System India Ltd', 'Zydus Wellness Ltd','Aditya Infotech Ltd'];                         
const REAL_COMPANY_TOKENS=['8727', '30108', '5385', '27061', '23729', '7', '5578', '756843', '757336', '25977', '11343', '1467', '25328', '11703', '163', '5378', '212', '11618', '14418', '5610', '757645', '263', '275', '19913', '368', '395', '17279', '19585', '757102', '383', '438', '10604', '23489', '11373', '19686', '8311', '2203', '15254', '628', '760', '20329', '8866', '685', '5049', '11543', '342', '18060', '4421', '1901', '811', '772', '827', '9599', '10940', '21690', '29452', '916', '919', '21154', '14450', '9383', '24398', '25162', '1041', '12032', '16783', '13528', '1186', '1153', '13409', '10099', '10925', '13560', '13750', '13197', '13966', '4244', '21951', '9819', '2056', '3417', '5622', '20988', '10726', '20261', '11262', '29135', '20607', '7852', '5926', '1633', '4986', '1726', '11655', '13637', '11236', '2783', '3637', '13260', '14912', '13310', '5108', '1949', '1814', '2955', '12092', '20936', '24948', '2606', '10440', '13285', '2031', '19061', '15380', '10999', '7242', '9581', '22308', '31181', '23650', '3918', '14672', '17433', '2406', '15815', '357', '18721', '10637', '6705', '29224', '756802', '6656', '25358', '16682', '13147', '9741', '18365', '14552', '2664', '11571', 
    '25718', '9590', '11403', '20302', '8825', '940', '9553', '18566', '14255', '18883', '3273', '27052', '27839', '4892', '31238', '17186', '756871', '13332', '4684', '7083', '17105', '3351', '3339', '3345', '3363', '12018', '27095', '10793', '8479', '3721', '6445', '7105', '3475', '19196', '14198', '15414', '3506', '3518', '11287', '14154', '8840', '15362', '28847', '27969', '14366', '756038', '7506', '3812', '7508', '27144', '7929', '758858', '4481', '1134', '9111', '15058', '3149', '5142', '757850', '11423', '758563', '27213', '20322', '13710', '1267', '29731', '1485', '21062', '22663', '25643', '8054', '14972', '18944', '199', '756324', '2972', '5911', '19631', '14922', '29711', '13414', '2816', '6643', '21501', '3387', '28805', '19184', '757965', '3324', '10945', '21828', '3703', '14766', '14602', '17738', '18608', '13061', '474', '13', '22', '25780', '21238', '17903', '10217', '25', '3563', '15083', '17388', '6066', '21614', '1270', '757885', '157', '5435', '236', '5900', '16669', '16675', '317', '305', '25270', '335', '2263', '4668', '11377', '17927', '404', '2144', '422', '526', '6435', '2181', '24814', '547', '757', '10794', '3906', '595', '21740', '5701', '20374', '21508', '15141', 
    '4749', '739', '17094', '14732', '8075', '910', '18822', '958', '5097', '1023', '1008', '11573', '14592', '4717', '13337', '277', '7406', '11956', '23799', '1181', '17875', '1232', '7229', '757772', '1333', '1348', '29666', '1363', '2303', '1406', '1394', '1424', '18457', '20825', '25844', '4963', '21770', '18652', '1476', '11184', '1491', '29251', '1660', '14309', '1512', '1624', '9348', '13611', '2029', '5258', '13751', '1594', '11195', '28125', '13270', '17869', '19020', '11723', '6733', '18143', '18096', '19126', '1196', '18581', '1922', '13816', '18564', '1997', '1979', '17818', '11483', '19234', '9480', '1627', '17313', '3220', '2277', '2283', '4067', '2142', '22377', '509', '8596', '14947', '4503', '17400', '15332', '27176', '11630', '11840', '6364', '17963', '5426', '20242', '2475', '17438', '24777', '10738', '24184', '14413', '17029', '11351', '14299', '14977', '25049', '2535', '21001', '15355', '10990', '9552', '2885', '3761', '17971', '21808', '4204', '1011', '3103', '4306', '3150', '13826', '3045', '2963', '9617', '27066', '11536', '3432', '3411', '1621', '3456', '3426', '3499', '13538', '2043', '13786', '1964', '312', '11223', '11532', '10753', '16713', '10447', '18921', 
    '3063', '3718', '25907', '3787', '11915', '1076', '15179', '11868', '13086', '8110', '625', '6018', '25984', '40', '8124', '24308', '100', '7145', '13620', '324', '2829', '11491', '193', '203', '1508', '15034', '14501', '371', '3834', '11966', '6994', '759291', '495', '380', '15184', '11452', '14937', '7603', '14966', '583', '5407', '1250', '14894', '14982', '13305', '8546', '637', '17945', '2854', '5748', '7358', '19943', '5373', '18086', '20551', '11654', '13643', '928', '937', '13517', '4907', '5382', '676', '3744', '1038', '14304', '5054', '1127', '1085', '5475', '1576', '144', '11778', '11971', '20534', '13776', '1235', '8828', '10599', '5204', '3892', '14334', '17939', '13072', '11809', '15313', '3329', '1675', '23693', '1515', '220', '4751', '28378', '1630', '15266', '13491', '11860', '11880', '11763', '5633', '2331', '3024', '20224', '15146', '21334', '13359', '15283', '9683', '1808', '758558', '4847', '18321', '25807', '29482', '17534', '2085', '18226', '31415', '2319', '8585', '4014', '2987', '399', '1164', '27097', '21469', '30089', '2649', '18908', '11355', '2643', '2705', '13496', '18391', '31163', '2431', '15337', '9408', '7401', '13451', '27297', '25073', '2859', '758551', 
    '20323', '128', '18026', '3186', '18614', '18359', '25222', '1442', '5751', '17758', '757014', '17271', '3078', '10530', '12026', '4693', '9428', '13631', '21091', '9309', '13404', '2183', '3348', '10243', '1581', '23740', '29008', '3405', '20293', '14223', '17032', '9117', '15174', '28714', '757545', '9685', '25584', '527', '3724', '20188', '2073', '8167', '17364', '11821', '11580', '18011', '16915', '17635','758858']
const REAL_COMPANY_SYMBOL=['MEDANTA-EQ','GICRE-EQ','MAHABANK-EQ','MFSL-EQ','JKCEMENT-EQ',
                         'HINDPETRO-EQ','FORTIS-EQ']




class Company {
    constructor(name, idx) {
        this.name = name;
        this.idx = idx;
        this.price = 100 + Math.floor(Math.random() * 1000);
        this.priceData = Array(376).fill(null);  // 9:15 to 15:30 = 376 minutes*/
        this.lastUpdatedIndex = -1;
         
        
    
    }

    
    getLatestPriceData() {
        return this.priceData;
    }

    getCurrentPrice() {
        return this.price;
    }
}

const companies = REAL_COMPANY_NAMES.slice(0, ).map((name, idx) => new Company(name, idx));
const companyListDiv = document.getElementById('companyList');

function renderCompanyList() {
    companyListDiv.innerHTML = '';
    companies.forEach((company, idx) => {
        const btn = document.createElement('button');
        btn.className = 'company-btn';
        btn.innerHTML = `<span id="com_name">${company.name}</span><span class="company-price" id="companyPriceList${idx}">₹${company.price}</span>`;
        
        btn.onclick = async () => {
        currentChart.stop();
        document.querySelectorAll('.company-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        await currentChart.setCompany(company); // ⬅ wait for history
        currentChart.start();                   // ⬅ plot AFTER data is ready
      };
        companyListDiv.appendChild(btn);
    });
    // ✅ Auto-click the first company button after rendering
    const firstBtn = companyListDiv.querySelector('.company-btn');
    if (firstBtn) firstBtn.click();

}

function getCurrentMinuteIndex() {
    const now = new Date();
    const marketStart = new Date();
    marketStart.setHours(9, 15, 0, 0);
    const marketEnd = new Date();
    marketEnd.setHours(15, 30, 0, 0);
    if (now > marketEnd) return 375;
    if (now < marketStart) return -1;
    const diff = Math.floor((now - marketStart) / 60000);
    return Math.min(Math.max(0, diff), 375);
}

// Replace with your actual API URL for live prices
const PRICE_API_URL = "/live-price-loop/"; 
(function(){
  // Use the existing global arrays/objects: companies, REAL_COMPANY_TOKENS, currentChart
  const wsScheme = (location.protocol === 'https:') ? 'wss' : 'ws';
  const socket = new WebSocket(wsScheme + '://' + window.location.host + '/ws/live-prices/');

  socket.addEventListener('open', (evt) => {
    console.log("WebSocket connected for live prices");
  });

  socket.addEventListener('message', (evt) => {
    try {
      const data = JSON.parse(evt.data);
      // data.type can be "prices_snapshot" (initial) or "prices_update" (periodic)
      const prices = data.prices || {};
      // prices is an object like {"11956": 523.75, "277": 314.20, ...}
      // Update company objects and UI similarly to polling approach
      companies.forEach((company, idx) => {
        const token = REAL_COMPANY_TOKENS[idx];
        if (token && prices[token] !== undefined) {
          company.price = prices[token];
          const timeIndex = getCurrentMinuteIndex();
          if (timeIndex >= 0 && timeIndex < company.priceData.length) {
            company.priceData[timeIndex] = company.price;
          }
          const priceSpan = document.getElementById(`companyPriceList${idx}`);
          if (priceSpan) priceSpan.textContent = `₹${company.price}`;
        }
      });

      // update currently shown chart
      if (typeof currentChart !== 'undefined' && currentChart) {
        currentChart.updateChart();
      }
    } catch (e) {
      console.error("WS parse error:", e, evt.data);
    }
  });

  socket.addEventListener('close', (evt) => {
    console.warn("WebSocket closed:", evt);
    // attempt reconnect with backoff
    attemptReconnect();
  });

  socket.addEventListener('error', (err) => {
    console.error("WebSocket error:", err);
    socket.close();
  });

  // Reconnect logic (simple exponential backoff)
  let reconnectAttempts = 0;
  function attemptReconnect() {
    reconnectAttempts++;
    const delay = Math.min(30, Math.pow(2, reconnectAttempts)) * 1000; // up to 30s
    console.log(`Attempting reconnect in ${delay/1000}s`);
    setTimeout(() => {
      // create new socket and reassign handlers by reloading page or re-executing setup
      window.location.reload(); // simplest option — refresh UI state and reconnect
    }, delay);
  }

  // Optional: expose socket for debugging
  window.__livePriceSocket = socket;
})();




// ---------------- CHART CLASS BELOW ----------------

class StockChart {
    constructor(chartId) {
        this.chartId = chartId;
        this.company = null;
        this.timeLabels = this.generateTimeLabels();
        this.priceData = Array(this.timeLabels.length).fill(null);
        this.lastPrice = 0;
        this.high = 0;
        this.low = 0;
        this.realTimeIndex = 0;
        this.interval = null;
    }
    async setCompany(company) {
    this.company = company;

    // Fetch full intraday data (9:15 → now)
    const token = REAL_COMPANY_TOKENS[company.idx];
    try {
        const response = await fetch(`/update-chart-array/${token}/`);
        const data = await response.json();

        // Store in company
        company.priceData = data.prices;

        // Copy to chart
        this.priceData = [...company.priceData];
    } catch (err) {
        console.error("Error fetching history:", err);
        this.priceData = [...company.priceData];
    }

    // Now calculate high/low properly
    const validPrices = this.priceData.filter(p => p !== null);
    this.lastPrice = validPrices.length ? validPrices.at(-1) : company.getCurrentPrice();
    this.high = validPrices.length ? Math.max(...validPrices) : this.lastPrice;
    this.low = validPrices.length ? Math.min(...validPrices) : this.lastPrice;
}

    

    generateTimeLabels() {
        const times = [];
        const start = new Date();
        start.setHours(9, 15, 0, 0);
        for (let i = 0; i <= 375; i++) {
            let t = new Date(start.getTime() + i * 60000);
            times.push(t.toTimeString().slice(0, 5));
        }
        return times;
    }

    generate30MinTicks() {
        const ticks = [];
        for (let i = 0; i <= 375; i += 30) {
            ticks.push(this.timeLabels[i]);
        }
        return ticks;
    }

    

    getCurrentMinuteIndex() {
        const now = new Date();
        const marketStart = new Date();
        marketStart.setHours(9, 15, 0, 0);
        const marketEnd = new Date();
        marketEnd.setHours(15, 30, 0, 0);
        if (now > marketEnd) return this.timeLabels.length - 1;
        if (now < marketStart) return -1;
        const diff = Math.floor((now - marketStart) / 60000);
        return Math.min(Math.max(0, diff), this.timeLabels.length - 1);
    }

    initializeChart() {
        const tickvals = this.generate30MinTicks();
        const trace = {
            x: this.timeLabels,
            y: this.priceData,
            type: 'line',
            mode: 'lines',
            connectgaps: true,
            line: { color: '#667eea', width: 2, shape: 'linear' },
            marker: { size: 4, color: '#764ba2', line: { color: '#fff', width: 1 } },
            name: 'Price',
            fill: 'tonexty',
            fillcolor: 'rgba(102, 126, 234, 0.1)',

             // 🔹 Customize hover
            hovertemplate: 'Time: %{x}<br>Price: ₹%{y:.2f}<extra></extra>',
            hoverlabel: {
                bgcolor: "#1f2937",  // dark background
                font: { color: "#ffffff", size: 12 }
            }
        };
        const layout = {
            xaxis: {
                range: [this.timeLabels[0], this.timeLabels[this.timeLabels.length - 1]],
                tickvals: tickvals,
                ticktext: tickvals,
                showgrid: false,
                zeroline: false,
                tickfont: { color: '#ffffff' },
                showspikes: true,       // enable spike line
                spikemode: 'across',    // show across plot
                spikecolor: 'white',    // 🔹 vertical line color
                spikethickness: 0,      // 🔹 line thickness
                spikedash: 'solid'      // style: 'solid', 'dot', 'dash'
            },
            yaxis: {
                range: [this.low, this.high],
                showgrid: false,
                zeroline: false,
                tickfont: { color: '#ffffff' },
                showspikes: true,
                spikemode: 'across',
                spikecolor: 'white',    // 🔹 horizontal spike color
                spikethickness: 0,
                spikedash: 'solid'

            },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            margin: { l: 30, r: 30, t: 20, b: 20 },
            hovermode: 'x',
            showlegend: false
        };
        
        const config = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            displaylogo: false
        };
        Plotly.newPlot(this.chartId, [trace], layout, config);
    }
   

    updateChart() {
        const timeIndex = this.getCurrentMinuteIndex();
        if (timeIndex >= 0 && timeIndex < this.timeLabels.length) {
            const newPrice = this.company.getCurrentPrice();
            this.priceData[timeIndex] = newPrice;
            this.lastPrice = newPrice;
            if (newPrice > this.high) this.high = newPrice;
            if (newPrice < this.low) this.low = newPrice;
            Plotly.update(this.chartId, { y: [this.priceData] });
            this.updateCompanyInfo();
        }
    }

    updateCompanyInfo() {
        if (!this.company) return;
        document.getElementById('companyName').textContent = this.company.name;
        document.getElementById('companyPrice').textContent = `₹${this.lastPrice}`;
        document.getElementById('highPrice').textContent = `1D high: ₹${this.high}`;
        document.getElementById('lowPrice').textContent = `1D low: ₹${this.low}`;
        const change = this.lastPrice - this.priceData[0];
        const percent = (((change) / this.lastPrice)* 100).toFixed(2);
        document.getElementById('priceChange').textContent = ` ₹${change.toFixed(2)}`;
        document.getElementById('percentChange').textContent = `${percent}%`;
    }

    start() {
        if (!this.company) return;
        this.initializeChart();
        this.updateCompanyInfo();
        if (this.interval) clearInterval(this.interval);
        this.interval = setInterval(() => this.updateChart(), 1000);
        window.addEventListener('resize', () => Plotly.Plots.resize(this.chartId));
    }

    stop() {
        if (this.interval) clearInterval(this.interval);
    }
}

// -------------- INIT --------------
const currentChart = new StockChart('chart');
waitForElement('#companyList', { timeout: 3000 })
  .then(companyList => {
    renderCompanyList(); // now it's guaranteed that companyList exists
  })
  .catch(err => console.warn(err));
update_chart_array();

currentChart.start();                  // Start its chart
});
});





