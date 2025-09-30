import pandas as pd
import numpy as np
import streamlit as st
import time
from datetime import datetime
import pydeck as pdk

# Create the updated hospitals dataset with all facilities
hospitals_data = {
    'facility_name': [
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Kisumu County Referral Hospital',
        'Lumumba Sub-County Hospital',
        'Ahero Sub-County Hospital',
        'Kombewa Sub-County / District Hospital',
        'Muhoroni County Hospital',
        'Nyakach Sub-County Hospital',
        'Chulaimbo Sub-County Hospital',
        'Masogo Sub-County (Sub-District) Hospital',
        'Nyando District Hospital',
        'Ober Kamoth Sub-County Hospital',
        'Rabuor Sub-County Hospital',
        'Nyangoma Sub-County Hospital',
        'Nyahera Sub-County Hospital',
        'Katito Sub-County Hospital',
        'Gita Sub-County Hospital',
        'Masogo Health Centre',
        'Victoria Hospital (public) Kisumu',
        'Kodiaga Prison Health Centre',
        'Kisumu District Hospital',
        'Migosi Health Centre',
        'Katito Health Centre',
        'Mbaka Oromo Health Centre',
        'Migere Health Centre',
        'Milenye Health Centre',
        'Minyange Dispensary',
        'Nduru Kadero Health Centre',
        'Newa Dispensary',
        'Nyakoko Dispensary',
        'Ojola Sub-County Hospital',
        'Simba Opepo Health Centre',
        'Songhor Health Centre',
        'St Marks Lela Health Centre',
        'Maseno University Health Centre',
        'Geta Health Centre',
        'Kadinda Health Centre',
        'Kochieng Health Centre',
        'Kodingo Health Centre',
        'Kolenyo Health Centre',
        'Kandu Health Centre'
    ],
    'latitude': [
        -0.0754, -0.0754, -0.1058, -0.1743, -0.1813, -0.1551, -0.2670,
        -0.1848, -0.1855, -0.3573, -0.3789, -0.2138, -0.1625, -0.1565,
        -0.4533, -0.3735, -0.1855, -0.0878, -0.0607, -0.0916, -0.1073,
        -0.4533, -0.2628, -0.1225, -0.1872, -0.2192, -0.1356, -0.2014,
        -0.2678, -0.1578, -0.3381, -0.2131, -0.0803, -0.0025, -0.4739,
        -0.2167, -0.3658, -0.0956, -0.4536, -0.2314
    ],
    'longitude': [
        34.7695, 34.7695, 34.7568, 34.9169, 34.6326, 35.1985, 35.0569,
        34.6163, 35.0386, 35.0006, 35.0299, 34.8817, 34.7794, 34.7508,
        34.9561, 34.9676, 35.0386, 34.7686, 34.7509, 34.7647, 34.7794,
        34.9561, 34.6061, 34.7553, 34.7781, 34.8331, 34.7381, 34.8289,
        34.9981, 34.8419, 34.9456, 35.1611, 34.6569, 34.6053, 34.9519,
        34.8419, 34.9606, 34.7658, 34.9564, 34.8489
    ],
    'facility_type': [
        'Referral Hospital', 'Referral Hospital', 'Sub-County Hospital', 
        'Sub-County Hospital', 'Sub-County Hospital', 'County Hospital',
        'Sub-County Hospital', 'Sub-County Hospital', 'Sub-County Hospital',
        'District Hospital', 'Sub-County Hospital', 'Sub-County Hospital',
        'Sub-County Hospital', 'Sub-County Hospital', 'Sub-County Hospital',
        'Sub-County Hospital', 'Health Centre', 'Private Hospital',
        'Prison Health Centre', 'District Hospital', 'Health Centre',
        'Health Centre', 'Health Centre', 'Health Centre', 'Health Centre',
        'Dispensary', 'Health Centre', 'Dispensary', 'Dispensary',
        'Sub-County Hospital', 'Health Centre', 'Health Centre', 'Health Centre',
        'University Health Centre', 'Health Centre', 'Health Centre',
        'Health Centre', 'Health Centre', 'Health Centre', 'Health Centre'
    ],
    'capacity': [
        500, 400, 100, 100, 100, 75, 75, 78, 77, 80, 70, 60, 65, 50, 52,
        40, 42, 30, 35, 20, 20, 25, 15, 24, 15, 10, 19, 5, 19, 10, 5, 15,
        17, 16, 45, 30, 29, 55, 30, 30
    ],
    'ambulance_services': [
        'Available', 'Available', 'Limited', 'Limited', 'Limited', 'Limited',
        'Limited', 'Limited', 'Limited', 'Limited', 'Limited', 'Limited',
        'Limited', 'Limited', 'Limited', 'Limited', 'Limited', 'Limited',
        'Limited', 'Limited', 'Limited', 'Limited', 'Limited', 'Limited',
        'Limited', 'Limited', 'Limited', 'Limited', 'Limited', 'Limited',
        'Limited', 'Limited', 'Limited', 'Limited', 'Limited', 'Limited',
        'Limited', 'Limited', 'Limited', 'Limited'
    ],
    'specialist_clinics': [
        'Yes', 'Yes', 'Basic Services', 'Basic Services', 'Basic Services',
        'Basic Services', 'Basic Services', 'Basic Services', 'Basic Services',
        'Basic Services', 'Basic Services', 'Basic Services', 'Basic Services',
        'Basic Services', 'Basic Services', 'Basic Services', 'Basic Services',
        'Basic Services', 'Basic Services', 'Basic Services', 'Basic Services',
        'Basic Services', 'Basic Services', 'Basic Services', 'Basic Services',
        'Basic Services', 'Basic Services', 'Basic Services', 'Basic Services',
        'Basic Services', 'Basic Services', 'Basic Services', 'Basic Services',
        'Basic Services', 'Basic Services', 'Basic Services', 'Basic Services',
        'Basic Services', 'Basic Services', 'Basic Services'
    ],
    'specialties_available': [
        'Cardiology, Surgery, Pediatrics, Orthopedics, ICU, Maternity, Emergency, Neurology, Oncology',
        'General Medicine, Surgery, Pediatrics, Maternity, ICU, Emergency',
        'General Medicine, Maternity, Emergency',
        'General Medicine, Maternity, Emergency',
        'General Medicine, Maternity',
        'General Medicine, Surgery, Maternity',
        'General Medicine, Maternity',
        'General Medicine, Maternity',
        'General Medicine, Maternity',
        'General Medicine, Surgery, Maternity',
        'General Medicine, Maternity',
        'General Medicine, Maternity',
        'General Medicine, Maternity',
        'General Medicine, Maternity',
        'General Medicine, Maternity',
        'General Medicine, Maternity',
        'Basic Healthcare',
        'General Medicine, Surgery',
        'Basic Healthcare',
        'General Medicine, Surgery, Maternity',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare',
        'Basic Healthcare'
    ]
}

hospitals_df = pd.DataFrame(hospitals_data)

# Create the updated ambulances dataset
ambulances_data = {
    'ambulance_id': [
        'KBA 453D', 'KBC 217F', 'KBD 389G', 'KBE 142H', 'KBF 561J', 
        'KBG 774K', 'KBH 238L', 'KBJ 965M', 'KBK 482N', 'KBL 751P',
        'KBM 312Q', 'KBN 864R', 'KBP 459S', 'KBQ 287T', 'KBR 913U',
        'KBS 506V', 'KBT 678W', 'KBU 134X', 'KBV 925Y', 'KBX 743Z'
    ],
    'current_location': [
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Jaramogi Oginga Odinga Teaching & Referral Hospital (JOOTRH)',
        'Kisumu County Referral Hospital',
        'Kisumu County Referral Hospital',
        'Kisumu County Referral Hospital',
        'Kisumu County Referral Hospital',
        'Kisumu County Referral Hospital',
        'Kisumu County Referral Hospital',
        'Kisumu County Referral Hospital',
        'Lumumba Sub-County Hospital',
        'Lumumba Sub-County Hospital',
        'Ahero Sub-County Hospital'
    ],
    'latitude': [
        -0.0754, -0.0754, -0.0754, -0.0754, -0.0754, -0.0754, -0.0754,
        -0.0754, -0.0754, -0.0754, -0.0754, -0.0754, -0.0754, -0.0754,
        -0.0754, -0.0754, -0.0754, -0.1058, -0.1058, -0.1743
    ],
    'longitude': [
        34.7695, 34.7695, 34.7695, 34.7695, 34.7695, 34.7695, 34.7695,
        34.7695, 34.7695, 34.7695, 34.7695, 34.7695, 34.7695, 34.7695,
        34.7695, 34.7695, 34.7695, 34.7568, 34.7568, 34.9169
    ],
    'status': [
        'Available', 'Available', 'Available', 'Available', 'Available',
        'Available', 'Available', 'Available', 'Available', 'Available',
        'Available', 'Available', 'Available', 'Available', 'Available',
        'Available', 'Available', 'Available', 'Available', 'Available'
    ],
    'driver_name': [
        'John Omondi', 'Mary Achieng', 'Paul Otieno', 'Susan Akinyi', 'David Owino',
        'James Okoth', 'Grace Atieno', 'Peter Onyango', 'Alice Adhiambo', 'Robert Ochieng',
        'Sarah Nyongesa', 'Michael Odhiambo', 'Elizabeth Awuor', 'Daniel Omondi', 'Lucy Anyango',
        'Brian Ouma', 'Patricia Adongo', 'Samuel Owuor', 'Rebecca Aoko', 'Kevin Onyango'
    ],
    'driver_contact': [
        '+254712345678', '+254723456789', '+254734567890', '+254745678901', '+254756789012',
        '+254767890123', '+254778901234', '+254789012345', '+254790123456', '+254701234567',
        '+254712345679', '+254723456780', '+254734567891', '+254745678902', '+254756789013',
        '+254767890124', '+254778901235', '+254789012346', '+254790123457', '+254701234568'
    ]
}

ambulances_df = pd.DataFrame(ambulances_data)

# The rest of your code remains the same (Patient class, Ambulance class, HospitalReferralSystem class, and display functions)
class Patient:
    def __init__(self, name, age, condition, referring_hospital, receiving_hospital, 
                 referring_physician, receiving_physician, notes):
        self.patient_id = f"PAT{np.random.randint(1000, 9999)}"
        self.name = name
        self.age = age
        self.condition = condition
        self.referring_hospital = referring_hospital
        self.receiving_hospital = receiving_hospital
        self.referring_physician = referring_physician
        self.receiving_physician = receiving_physician
        self.notes = notes
        self.vital_signs = {}
        self.medical_history = ""
        self.current_medications = ""
        self.allergies = ""
        self.referral_time = datetime.now()
        self.status = "Referred"
        self.assigned_ambulance = None
        
    def update_vital_signs(self, bp, heart_rate, temperature, spo2):
        self.vital_signs = {
            'blood_pressure': bp,
            'heart_rate': heart_rate,
            'temperature': temperature,
            'oxygen_saturation': spo2
        }
    
    def add_medical_info(self, history, medications, allergies):
        self.medical_history = history
        self.current_medications = medications
        self.allergies = allergies
    
    def to_dict(self):
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'age': self.age,
            'condition': self.condition,
            'referring_hospital': self.referring_hospital,
            'receiving_hospital': self.receiving_hospital,
            'referring_physician': self.referring_physician,
            'receiving_physician': self.receiving_physician,
            'notes': self.notes,
            'vital_signs': self.vital_signs,
            'medical_history': self.medical_history,
            'current_medications': self.current_medications,
            'allergies': self.allergies,
            'referral_time': self.referral_time,
            'status': self.status,
            'assigned_ambulance': self.assigned_ambulance
        }

class Ambulance:
    def __init__(self, ambulance_id, current_location, latitude, longitude, status, driver_name, driver_contact):
        self.ambulance_id = ambulance_id
        self.current_location = current_location
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.driver_name = driver_name
        self.driver_contact = driver_contact
        self.current_patient = None
        self.destination = None
        self.route = []
        self.start_time = None
        self.current_step = 0
        self.mission_complete = False
        
    def assign_mission(self, patient, referring_hospital_lat, referring_hospital_lon, 
                      receiving_hospital_lat, receiving_hospital_lon):
        self.current_patient = patient
        self.destination = patient.receiving_hospital
        self.status = "On Transfer"
        self.start_time = datetime.now()
        self.current_step = 0
        self.mission_complete = False
        
        # Calculate route from current position to referring hospital, then to receiving hospital
        self.calculate_route(referring_hospital_lat, referring_hospital_lon, 
                           receiving_hospital_lat, receiving_hospital_lon)
        patient.status = "Ambulance Dispatched"
        patient.assigned_ambulance = self.ambulance_id
        
    def calculate_route(self, ref_lat, ref_lon, rec_lat, rec_lon):
        # Route from current position to referring hospital
        steps1 = 5
        route_part1 = []
        for i in range(steps1 + 1):
            lat = self.latitude + (ref_lat - self.latitude) * (i / steps1)
            lon = self.longitude + (ref_lon - self.longitude) * (i / steps1)
            route_part1.append((lat, lon))
        
        # Route from referring hospital to receiving hospital
        steps2 = 10
        route_part2 = []
        for i in range(steps2 + 1):
            lat = ref_lat + (rec_lat - ref_lat) * (i / steps2)
            lon = ref_lon + (rec_lon - ref_lon) * (i / steps2)
            route_part2.append((lat, lon))
        
        self.route = route_part1 + route_part2[1:]  # Skip duplicate point
    
    def update_position(self):
        if self.current_step < len(self.route):
            self.latitude, self.longitude = self.route[self.current_step]
            self.current_step += 1
            
            # Update patient status based on progress
            if self.current_patient:
                if self.current_step < len(self.route) // 2:
                    self.current_patient.status = "Ambulance En Route to Patient"
                elif self.current_step == len(self.route) // 2:
                    self.current_patient.status = "Patient Picked Up"
                elif self.current_step < len(self.route):
                    self.current_patient.status = "Transporting to Destination"
                else:
                    self.current_patient.status = "Arrived at Destination"
                    self.status = "Available"
                    self.mission_complete = True
            return True
        else:
            if self.current_patient:
                self.current_patient.status = "Arrived at Destination"
            self.status = "Available"
            self.mission_complete = True
            return False
    
    def complete_mission(self):
        self.current_patient = None
        self.destination = None
        self.route = []
        self.status = "Available"
        self.start_time = None
        self.current_step = 0
        self.mission_complete = False

class HospitalReferralSystem:
    def __init__(self, hospitals_df, ambulances_df):
        self.hospitals = hospitals_df
        self.ambulances_df = ambulances_df
        self.ambulances = []
        self._initialize_ambulances()
        self.patients = []
        self.referrals = []
        self.messages = []
        self.handover_forms = []
        
    def _initialize_ambulances(self):
        for _, ambulance_data in self.ambulances_df.iterrows():
            ambulance = Ambulance(
                ambulance_data['ambulance_id'],
                ambulance_data['current_location'],
                ambulance_data['latitude'],
                ambulance_data['longitude'],
                ambulance_data['status'],
                ambulance_data['driver_name'],
                ambulance_data['driver_contact']
            )
            self.ambulances.append(ambulance)
    
    def find_available_ambulances(self):
        return [amb for amb in self.ambulances if amb.status == 'Available']
    
    def get_ambulance_by_id(self, ambulance_id):
        for ambulance in self.ambulances:
            if ambulance.ambulance_id == ambulance_id:
                return ambulance
        return None
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate approximate distance between two points (simplified)"""
        return np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 111  # Approximate km
    
    def create_referral(self, patient, selected_ambulance_id):
        """Create a new patient referral and assign ambulance"""
        # Find the selected ambulance
        ambulance = self.get_ambulance_by_id(selected_ambulance_id)
        if not ambulance:
            return None, "Ambulance not found"
        
        # Get hospital coordinates
        referring_hospital = self.hospitals[
            self.hospitals['facility_name'] == patient.referring_hospital
        ].iloc[0]
        
        receiving_hospital = self.hospitals[
            self.hospitals['facility_name'] == patient.receiving_hospital
        ].iloc[0]
        
        # Assign mission to ambulance
        ambulance.assign_mission(
            patient,
            referring_hospital['latitude'],
            referring_hospital['longitude'],
            receiving_hospital['latitude'],
            receiving_hospital['longitude']
        )
        
        self.patients.append(patient)
        self.referrals.append({
            'patient_id': patient.patient_id,
            'timestamp': datetime.now(),
            'status': 'Ambulance Dispatched',
            'ambulance_id': selected_ambulance_id
        })
        
        # Send notification
        self.send_message(
            patient.referring_hospital,
            patient.receiving_hospital,
            f"Patient {patient.name} referred. Ambulance {selected_ambulance_id} dispatched.",
            patient.patient_id
        )
        
        return patient.patient_id, "Referral created successfully"
    
    def send_message(self, from_hospital, to_hospital, message, patient_id=None):
        """Send message between hospitals"""
        message_obj = {
            'from': from_hospital,
            'to': to_hospital,
            'message': message,
            'patient_id': patient_id,
            'timestamp': datetime.now(),
            'read': False
        }
        self.messages.append(message_obj)
        return message_obj
    
    def get_messages(self, hospital_name):
        """Get messages for a specific hospital"""
        hospital_messages = [msg for msg in self.messages if msg['to'] == hospital_name]
        return hospital_messages
    
    def mark_message_read(self, message_index):
        """Mark a message as read"""
        if message_index < len(self.messages):
            self.messages[message_index]['read'] = True
    
    def create_handover_form(self, patient_id):
        """Create handover form when patient arrives"""
        patient = next((p for p in self.patients if p.patient_id == patient_id), None)
        if not patient:
            return None
        
        handover_form = {
            'patient_id': patient.patient_id,
            'patient_name': patient.name,
            'age': patient.age,
            'condition': patient.condition,
            'referring_hospital': patient.referring_hospital,
            'receiving_hospital': patient.receiving_hospital,
            'referring_physician': patient.referring_physician,
            'receiving_physician': patient.receiving_physician,
            'transfer_time': datetime.now(),
            'vital_signs': patient.vital_signs,
            'medical_history': patient.medical_history,
            'current_medications': patient.current_medications,
            'allergies': patient.allergies,
            'notes': patient.notes,
            'ambulance_id': patient.assigned_ambulance
        }
        
        self.handover_forms.append(handover_form)
        return handover_form

def display_live_map(system):
    """Display interactive map with hospitals and ambulances using PyDeck"""
    
    # Prepare hospital data
    hospital_data = []
    for _, hospital in system.hospitals.iterrows():
        hospital_data.append({
            'name': hospital['facility_name'],
            'lat': hospital['latitude'],
            'lon': hospital['longitude'],
            'type': hospital['facility_type'],
            'color': [0, 128, 0]  # Green for hospitals
        })
    
    # Prepare ambulance data
    ambulance_data = []
    for ambulance in system.ambulances:
        if ambulance.status == 'Available':
            color = [0, 0, 255]  # Blue
        elif ambulance.status == 'On Transfer':
            color = [255, 0, 0]  # Red
        else:
            color = [128, 128, 128]  # Gray
            
        ambulance_data.append({
            'name': f"Ambulance {ambulance.ambulance_id}",
            'lat': ambulance.latitude,
            'lon': ambulance.longitude,
            'status': ambulance.status,
            'driver': ambulance.driver_name,
            'color': color,
            'patient': ambulance.current_patient.name if ambulance.current_patient else 'None'
        })
    
    # Combine all data
    all_data = hospital_data + ambulance_data
    
    if all_data:
        # Create PyDeck layer
        layer = pdk.Layer(
            'ScatterplotLayer',
            all_data,
            get_position=['lon', 'lat'],
            get_color='color',
            get_radius=200,
            pickable=True,
            auto_highlight=True,
        )
        
        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=34.7680,
            latitude=-0.0916,
            zoom=10,
            pitch=0,
            bearing=0
        )
        
        # Render the map
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                'html': '''
                    <b>Name:</b> {name}<br/>
                    <b>Type:</b> {type}<br/>
                    <b>Status:</b> {status}<br/>
                    <b>Driver:</b> {driver}<br/>
                    <b>Patient:</b> {patient}
                ''',
                'style': {
                    'color': 'white'
                }
            }
        )
        
        st.pydeck_chart(r)
    else:
        st.info("No data available for map")

def display_dashboard():
    st.header("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Hospitals", len(st.session_state.system.hospitals))
    with col2:
        available_ambulances = len(st.session_state.system.find_available_ambulances())
        st.metric("Available Ambulances", available_ambulances)
    with col3:
        active_referrals = len([p for p in st.session_state.system.patients if p.status != "Arrived at Destination"])
        st.metric("Active Referrals", active_referrals)
    with col4:
        pending_messages = len([m for m in st.session_state.system.messages if not m['read']])
        st.metric("Pending Messages", pending_messages)

    # Display map
    st.subheader("Hospital & Ambulance Locations")
    display_live_map(st.session_state.system)

def display_patient_referral():
    st.header("Create Patient Referral")

    # Initialize session state for patient data if not exists
    if 'temp_patient_data' not in st.session_state:
        st.session_state.temp_patient_data = None

    with st.form("patient_referral_form"):
        col1, col2 = st.columns(2)

        with col1:
            patient_name = st.text_input("Patient Name*", placeholder="Enter patient full name")
            age = st.number_input("Age*", min_value=0, max_value=120, value=30)
            
            # Condition options
            condition_options = [
                "Cardiac Emergency", "Trauma", "Stroke", "Respiratory Distress",
                "Severe Infection", "Surgical Emergency", "Obstetric Emergency",
                "Pediatric Emergency", "Neurological Emergency", "Other"
            ]
            condition = st.selectbox("Medical Condition*", condition_options)
            
            referring_hospital = st.selectbox(
                "Referring Hospital*",
                st.session_state.system.hospitals['facility_name'].tolist()
            )
            
            receiving_hospital = st.selectbox(
                "Receiving Hospital*",
                st.session_state.system.hospitals['facility_name'].tolist()
            )

        with col2:
            referring_physician = st.text_input("Referring Physician Name*", placeholder="Dr. Name")
            receiving_physician = st.text_input("Receiving Physician Name", placeholder="Dr. Name (if known)")
            
            notes = st.text_area("Clinical Notes*", placeholder="Brief summary of patient condition, reason for referral...", height=100)

            # Vital signs
            st.subheader("Vital Signs (Optional)")
            bp = st.text_input("Blood Pressure", "120/80")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, max_value=200, value=72)
            temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=43.0, value=36.6)
            spo2 = st.number_input("Oxygen Saturation (%)", min_value=0, max_value=100, value=98)

        submitted = st.form_submit_button("Continue to Ambulance Selection")

    # Handle form submission
    if submitted:
        # Validate required fields
        if not all([patient_name, condition, referring_hospital, receiving_hospital, referring_physician, notes]):
            st.error("Please fill in all required fields (*)")
        elif referring_hospital == receiving_hospital:
            st.error("Referring and receiving hospitals cannot be the same")
        else:
            # Store patient data in session state
            st.session_state.temp_patient_data = {
                'name': patient_name,
                'age': age,
                'condition': condition,
                'referring_hospital': referring_hospital,
                'receiving_hospital': receiving_hospital,
                'referring_physician': referring_physician,
                'receiving_physician': receiving_physician,
                'notes': notes,
                'bp': bp,
                'heart_rate': heart_rate,
                'temperature': temperature,
                'spo2': spo2
            }
            st.success("✅ Patient information saved. Please select an ambulance below.")

    # Show ambulance selection if we have patient data
    if st.session_state.temp_patient_data:
        st.subheader("Select Ambulance for Dispatch")
        
        available_ambulances = st.session_state.system.find_available_ambulances()
        if available_ambulances:
            ambulance_options = {f"{amb.ambulance_id} - {amb.driver_name} ({amb.current_location})": amb.ambulance_id 
                               for amb in available_ambulances}
            
            selected_ambulance_key = st.selectbox("Select Ambulance*", list(ambulance_options.keys()))
            selected_ambulance_id = ambulance_options[selected_ambulance_key]
            
            if st.button("Confirm Referral & Dispatch Ambulance"):
                # Create patient object
                patient_data = st.session_state.temp_patient_data
                patient = Patient(
                    patient_data['name'], 
                    patient_data['age'], 
                    patient_data['condition'], 
                    patient_data['referring_hospital'], 
                    patient_data['receiving_hospital'], 
                    patient_data['referring_physician'], 
                    patient_data['receiving_physician'], 
                    patient_data['notes']
                )
                patient.update_vital_signs(
                    patient_data['bp'], 
                    patient_data['heart_rate'], 
                    patient_data['temperature'], 
                    patient_data['spo2']
                )

                # Create referral and dispatch ambulance
                patient_id, message = st.session_state.system.create_referral(patient, selected_ambulance_id)
                
                if patient_id:
                    st.success(f"✅ Referral created for {patient_data['name']} (ID: {patient_id})")
                    st.success(f"🚑 Ambulance {selected_ambulance_id} dispatched!")
                    
                    # Show referral details
                    with st.expander("View Referral Details"):
                        st.write(f"**Patient ID:** {patient_id}")
                        st.write(f"**Name:** {patient_data['name']}")
                        st.write(f"**Condition:** {patient_data['condition']}")
                        st.write(f"**From:** {patient_data['referring_hospital']}")
                        st.write(f"**To:** {patient_data['receiving_hospital']}")
                        st.write(f"**Referring Physician:** {patient_data['referring_physician']}")
                        st.write(f"**Ambulance:** {selected_ambulance_id}")
                        st.write(f"**Status:** Ambulance Dispatched")
                    
                    # Clear temporary data
                    st.session_state.temp_patient_data = None
                    
                    # Auto-start simulation
                    st.session_state.simulation_running = True
                    st.rerun()
                else:
                    st.error(f"Failed to create referral: {message}")
        else:
            st.error("❌ No available ambulances at the moment. Please try again later.")
            
            # Option to clear and start over
            if st.button("Clear Form and Start Over"):
                st.session_state.temp_patient_data = None
                st.rerun()

def display_ambulance_tracking():
    st.header("Live Ambulance Tracking")
    
    # Update ambulance positions if simulation is running
    if st.session_state.simulation_running:
        current_time = datetime.now()
        if (current_time - st.session_state.last_update).seconds >= 2:  # Update every 2 seconds
            for ambulance in st.session_state.system.ambulances:
                if ambulance.status == "On Transfer":
                    ambulance.update_position()
                    
                    # Check if mission is complete and create handover form
                    if ambulance.mission_complete and ambulance.current_patient:
                        st.session_state.system.create_handover_form(ambulance.current_patient.patient_id)
            
            st.session_state.last_update = current_time
            st.rerun()

    # Simulation controls
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("▶ Start Simulation") and not st.session_state.simulation_running:
            st.session_state.simulation_running = True
            st.session_state.last_update = datetime.now()
            st.rerun()

        if st.button("⏹ Stop Simulation") and st.session_state.simulation_running:
            st.session_state.simulation_running = False
            st.rerun()

    # Display active transfers
    active_transfers = [amb for amb in st.session_state.system.ambulances if amb.status == "On Transfer"]
    if active_transfers:
        st.subheader("Active Transfers")
        for ambulance in active_transfers:
            with st.expander(f"🚑 {ambulance.ambulance_id} - {ambulance.driver_name}"):
                if ambulance.current_patient:
                    st.write(f"**Patient:** {ambulance.current_patient.name}")
                    st.write(f"**From:** {ambulance.current_patient.referring_hospital}")
                    st.write(f"**To:** {ambulance.destination}")
                    st.write(f"**Status:** {ambulance.current_patient.status}")
                    st.write(f"**Progress:** {ambulance.current_step}/{len(ambulance.route)} steps")
                    
                    # Progress bar
                    progress = ambulance.current_step / len(ambulance.route)
                    st.progress(progress)
                    
                    if ambulance.mission_complete:
                        st.success("✅ Mission Complete - Patient delivered!")
    else:
        st.info("No active transfers at the moment")

    # Display ambulance status table
    st.subheader("Ambulance Status")
    ambulance_data = []
    for ambulance in st.session_state.system.ambulances:
        ambulance_data.append({
            'Ambulance ID': ambulance.ambulance_id,
            'Driver': ambulance.driver_name,
            'Contact': ambulance.driver_contact,
            'Status': ambulance.status,
            'Current Location': ambulance.current_location,
            'Patient': ambulance.current_patient.name if ambulance.current_patient else "None"
        })
    
    if ambulance_data:
        st.dataframe(pd.DataFrame(ambulance_data))
    else:
        st.info("No ambulance data available")

    # Display live map
    st.subheader("Live Map")
    display_live_map(st.session_state.system)

def display_handover_forms():
    st.header("Patient Handover Forms")
    
    if st.session_state.system.handover_forms:
        for i, form in enumerate(st.session_state.system.handover_forms):
            with st.expander(f"Handover Form - {form['patient_name']} ({form['patient_id']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Patient Information")
                    st.write(f"**Patient ID:** {form['patient_id']}")
                    st.write(f"**Name:** {form['patient_name']}")
                    st.write(f"**Age:** {form['age']}")
                    st.write(f"**Condition:** {form['condition']}")
                    
                    st.subheader("Transfer Details")
                    st.write(f"**Referring Hospital:** {form['referring_hospital']}")
                    st.write(f"**Receiving Hospital:** {form['receiving_hospital']}")
                    st.write(f"**Referring Physician:** {form['referring_physician']}")
                    st.write(f"**Receiving Physician:** {form['receiving_physician']}")
                    st.write(f"**Transfer Time:** {form['transfer_time'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Ambulance:** {form['ambulance_id']}")
                
                with col2:
                    st.subheader("Clinical Information")
                    st.write("**Vital Signs:**")
                    for key, value in form['vital_signs'].items():
                        st.write(f"  - {key.replace('_', ' ').title()}: {value}")
                    
                    if form['medical_history']:
                        st.write(f"**Medical History:** {form['medical_history']}")
                    if form['current_medications']:
                        st.write(f"**Current Medications:** {form['current_medications']}")
                    if form['allergies']:
                        st.write(f"**Allergies:** {form['allergies']}")
                    
                    st.write(f"**Clinical Notes:** {form['notes']}")
                
                # Download button for handover form
                form_text = f"""
PATIENT HANDOVER FORM
=====================
Patient ID: {form['patient_id']}
Name: {form['patient_name']}
Age: {form['age']}
Condition: {form['condition']}

TRANSFER DETAILS
----------------
Referring Hospital: {form['referring_hospital']}
Receiving Hospital: {form['receiving_hospital']}
Referring Physician: {form['referring_physician']}
Receiving Physician: {form['receiving_physician']}
Transfer Time: {form['transfer_time'].strftime('%Y-%m-%d %H:%M')}
Ambulance: {form['ambulance_id']}

CLINICAL INFORMATION
-------------------
Vital Signs:
  - Blood Pressure: {form['vital_signs'].get('blood_pressure', 'N/A')}
  - Heart Rate: {form['vital_signs'].get('heart_rate', 'N/A')}
  - Temperature: {form['vital_signs'].get('temperature', 'N/A')}
  - Oxygen Saturation: {form['vital_signs'].get('oxygen_saturation', 'N/A')}

Medical History: {form['medical_history'] or 'N/A'}
Current Medications: {form['current_medications'] or 'N/A'}
Allergies: {form['allergies'] or 'N/A'}

Clinical Notes: {form['notes']}
"""
                
                st.download_button(
                    label="📄 Download Handover Form",
                    data=form_text,
                    file_name=f"handover_{form['patient_id']}.txt",
                    key=f"download_{i}"
                )
    else:
        st.info("No handover forms available yet. Forms are automatically created when patients arrive at their destination.")

def display_communication():
    st.header("Hospital Communication")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Send Message")

        with st.form("send_message_form"):
            from_hospital = st.selectbox(
                "From Hospital",
                st.session_state.system.hospitals['facility_name'].tolist()
            )
            to_hospital = st.selectbox(
                "To Hospital",
                st.session_state.system.hospitals['facility_name'].tolist()
            )
            patient_id = st.selectbox(
                "Patient (Optional)",
                [""] + [p.patient_id for p in st.session_state.system.patients]
            )
            message = st.text_area("Message")

            if st.form_submit_button("Send Message"):
                if message:
                    st.session_state.system.send_message(from_hospital, to_hospital, message, patient_id if patient_id else None)
                    st.success("Message sent successfully!")

    with col2:
        st.subheader("Received Messages")

        hospital_name = st.selectbox(
            "Select Your Hospital",
            st.session_state.system.hospitals['facility_name'].tolist(),
            key="message_hospital"
        )

        messages = st.session_state.system.get_messages(hospital_name)

        if not messages:
            st.info("No messages received")
        else:
            for i, msg in enumerate(messages):
                with st.expander(f"📩 Message from {msg['from']} - {msg['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                    st.write(f"**Patient ID:** {msg['patient_id'] if msg['patient_id'] else 'N/A'}")
                    st.write(f"**Message:** {msg['message']}")
                    if not msg['read']:
                        if st.button("Mark as Read", key=f"read_{i}"):
                            st.session_state.system.mark_message_read(
                                st.session_state.system.messages.index(msg)
                            )
                            st.rerun()

def display_reports():
    st.header("Reports & Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Patient Referrals")
        if st.session_state.system.patients:
            patients_data = [p.to_dict() for p in st.session_state.system.patients]
            patients_df = pd.DataFrame(patients_data)
            st.dataframe(patients_df[['patient_id', 'name', 'condition', 'referring_hospital', 'receiving_hospital', 'status']])
        else:
            st.info("No patient referrals yet")

    with col2:
        st.subheader("Referral Statistics")

        if st.session_state.system.patients:
            status_counts = pd.Series([p.status for p in st.session_state.system.patients]).value_counts()
            st.bar_chart(status_counts)

            condition_counts = pd.Series([p.condition for p in st.session_state.system.patients]).value_counts()
            st.write("**Referrals by Condition:**")
            st.dataframe(condition_counts)
        else:
            st.info("No data available for statistics")

def main():
    st.set_page_config(page_title="Kisumu County Hospital Referral System", layout="wide")

    st.title("🏥 Kisumu County Hospital Referral & Ambulance Tracking System")

    # Initialize session state
    if 'system' not in st.session_state:
        st.session_state.system = HospitalReferralSystem(hospitals_df, ambulances_df)
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = False
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    if 'temp_patient_data' not in st.session_state:
        st.session_state.temp_patient_data = None

    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Dashboard",
        "📋 Create Referral",
        "🚑 Ambulance Tracking",
        "📄 Handover Forms",
        "💬 Communication",
        "📊 Reports"
    ])

    with tab1:
        display_dashboard()

    with tab2:
        display_patient_referral()

    with tab3:
        display_ambulance_tracking()

    with tab4:
        display_handover_forms()

    with tab5:
        display_communication()

    with tab6:
        display_reports()

if __name__ == "__main__":
    main()