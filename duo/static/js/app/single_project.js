const { createApp } = Vue;

const app = createApp({
  data() {
    return {
      project: {
        "id": null,
        "name": "",
        "client": "",
        "contact": "",
        "start_date": "",
        "end_date": null,
        "status": "",
        "cost": null,
        "status_display": "",
        "note": "",
        "advances":[
            {   "id": null,
                "amount": "",
                "date": "",
                "note": "",
                "method": ""
            }],
        "offers": [
            {
                "id": null,
                "file": "",
                "description": "",
                "uploaded_at": ""
            }],
        "materials": [
            {
                "id": null,
                "project": null,
                "type_display": "",
                "quantity": "",
                "unit": null,
                "unit_display": "",
                "price": null,
                "note": "",
                "date": ""
            }],
        "workers": [
            {
                "id": null,
                "project": null,
                "name": "",
                "position": "",
                "cost": null
            }
        ]
      },
      sections: {
        offer: false,
        avans: false,
        materials: false,
        workers: false,
      },
      sectionList: [
        { key: 'offer', title: 'Ponuda' },
        { key: 'avans', title: 'Avans' },
        { key: 'materials', title: 'Materijali' },
        { key: 'workers', title: 'Radnici' },
      ],
      selectedMaterialType: [],
      selectedUnits: [],
      formAvans: {
        date: '',
        amount: '',
        payment: 'Keš',
        description: ''
      },
      formOffer: {
        file: null,
        description: ''
      },
      formMaterial: {
        type: null,
        quantity: '',
        unit: null,
        price: null,
        note: '',
        date: '',
      },
      formProject: {
        "id": null,
        "name": "",
        "client": "",
        "contact": "",
        "start_date": null,
        "end_date": null,
        "status": "",
        "cost": null,
        "note": ""
      },
      formWorker:{
        "name": '',
        "position": '',
        "cost": null,
      },
      activeModal: null,
      showProfit: false,
      showBruto: false,
    };
  },
  methods: {
    handleFileUpload(event) {
        this.formOffer.file = event.target.files[0];
    },
    toggleSection(name) {
      this.sections[name] = !this.sections[name];
    },
    async openModal(section) {
      if (section=='materials'){
        this.selectedMaterialType = await this.getJson('/construction/api/material-types/');
        this.selectedUnits = await this.getJson('/construction/api/units/');
      }
      if(section=='project'){
        this.fetchProject();
      }
      this.activeModal = section;
    },
    closeModal() {
      this.activeModal = null;
    },
    submitForm(formName, url, method='POST') {
      const form = this[formName];

      if (!form) {
        console.error(`Forma "${formName}" ne postoji.`);
        return;
      }

      // Dodaj project.id ako treba
      const payload = { ...form };
      if (!payload.project && this.project?.id) {
        payload.project = this.project.id;
      }

      fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCsrfToken()
        },
        body: JSON.stringify(payload)
      })
        .then(res => {

        })
        .then(responseData => {
          console.log(`Uspešan submit forme "${formName}"`, responseData);
          this.fetchProject();
          this.closeModal();

          // Resetuj formu
          for (let key in this[formName]) {
            this[formName][key] = '';
          }
          // Opciono: refresh sekcija
        })
        .catch(error => {
          console.error(`Greška pri slanju "${formName}":`, error);
        });
    },
    submitFormData(formName, url) {
      const form = this[formName];

      if (!form) {
        console.error(`Forma "${formName}" ne postoji.`);
        return;
      }

      // Pravimo FormData objekat i punimo ga podacima iz forme
      const formData = new FormData();

      for (const key in form) {
        if (form[key] !== null && form[key] !== undefined) {
          // Ako je polje fajl i ima više fajlova (npr. <input multiple>)
          if (form[key] instanceof FileList) {
            for (let i = 0; i < form[key].length; i++) {
              formData.append(key, form[key][i]);
            }
          } else {
            formData.append(key, form[key]);
          }
        }
      }

      // Ako ti treba project_id posebno:
      if (!form.project && this.project?.id) {
        formData.append('project', this.project.id);
      }

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
          // NE postavljaj Content-Type, browser će ga sam dodati
        },
        body: formData,
      })
        .then(res => {
          if (!res.ok) throw new Error('Greška pri slanju FormData forme');
          return res.json();
        })
        .then(data => {
          console.log('Uspešan upload fajla', data);
          this.fetchProject();
          this.closeModal();

          // Resetuj formu
          for (const key in form) {
            this[formName][key] = '';
          }
        })
        .catch(err => {
          console.error('Greška pri slanju forme:', err);
        });
    },
    async getJson(url) {
      this.loading = true;
      this.error = null;
      this.data = null;

      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Status: ${response.status}`);
        const json = await response.json();
        return json;
      } catch (err) {
        this.error = err.message;
        return null;
      } finally {
        this.loading = false;
      }
    },
    statusClass(status) {
        switch (status) {
          case 'planned':
            return 'bg-blue-400 text-white';
          case 'active':
            return 'bg-green-400 text-white';
          case 'paused':
            return 'bg-yellow-400 text-white';
          case 'completed':
            return 'bg-gray-400 text-white';
          case 'cancelled':
            return 'bg-red-400 text-white';
          default:
            return 'bg-gray-400 text-white';
        }
    },
    getCsrfToken() {
      const name = 'csrftoken';
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const c = cookies[i].trim();
        if (c.startsWith(name + '=')) {
          return decodeURIComponent(c.substring(name.length + 1));
        }
      }
      return '';
    },
    fetchProject(){
        const projectId = window.location.pathname.split('/').filter(Boolean).pop();

        fetch('/construction/api/project/' + projectId)
          .then(res => res.json())
          .then(data => {

            this.project = data;
            Object.keys(this.formProject).forEach(key => {
              if (data.hasOwnProperty(key)) {
                this.formProject[key] = data[key];
              }
            });

          })
          .catch(err => console.error('Greška pri dohvatanju projekata:', err));
    },
    deleteObject(url, id, callback = null) {
        if (!confirm("Da li ste sigurni da želite da obrišete ovaj podatak?")) return;

        fetch(`${url}${id}/`, {
          method: 'DELETE',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCsrfToken()
          }
        })
        .then(response => {
          if (response.ok) {
            if (callback) callback(id); // pozovi funkciju da ažurira prikaz
          } else {
            alert("Greška prilikom brisanja.");
          }
        })
        .catch(error => {
          console.error("Greška pri DELETE:", error);
        });
    },
    deleteOffer(id) {
        this.deleteObject('/construction/api/offers/', id, (deletedId) => {
//          this.project.offers = this.project.offers.filter(o => o.id !== deletedId);
             this.fetchProject();
        });
      },
    deleteAdvance(id) {
        this.deleteObject('/construction/api/advances/', id, (deletedId) => {
//          this.project.advances = this.project.advances.filter(o => o.id !== deletedId);
            this.fetchProject();
        });
      },
    deleteMaterial(id) {
        this.deleteObject('/construction/api/materials/', id, (deletedId) => {
//          this.project.materials = this.project.materials.filter(o => o.id !== deletedId);
            this.fetchProject();
        });
    },
    deleteWorker(id) {
        this.deleteObject('/construction/api/workers/', id, (deletedId) => {
//          this.project.materials = this.project.materials.filter(o => o.id !== deletedId);
            this.fetchProject();
        });
      },
  },
  mounted() {
    this.fetchProject();
  },
});

app.config.compilerOptions.delimiters = ['[[', ']]'];
app.mount('#single_project');
