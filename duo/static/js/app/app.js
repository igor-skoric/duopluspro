const { createApp } = Vue;

const app = createApp({
  data() {
    return {
      searchQuery: '',
      statusFilter: '',
      projects: [],
      activeModal: null,
      formProject: {
        "id": null,
        "name": "",
        "client": "",
        "contact": "",
        "start_date": "",
        "end_date": null,
        "status": "",
        "note": ""
      },
      sections: {
        addProject: true,
      },
      nextPage: null,
      prevPage: null,
      totalCount: 0,
      currentPage: 1,
      pageSize: 10, // koliko po stranici
    };
  },
  mounted() {
    this.fetchProjects();
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return '/'; // ili 'N/A', 'Nepoznat datum', ''

      const date = new Date(dateStr);
      if (isNaN(date)) return '/';

      return date.toLocaleDateString('sr-RS');
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
    openModal(section) {
      this.activeModal = section;
    },
    fetchProjects(page = 1) {
        const query = this.searchQuery ? `&search=${encodeURIComponent(this.searchQuery)}` : '';

        const url = `/construction/api/projects/?page=${page}&page_size=${this.pageSize}${query}`;

        fetch(url)
          .then(res => res.json())
          .then(data => {
            this.projects = data.results;
            this.totalCount = data.count;
            this.nextPage = data.next;
            this.prevPage = data.previous;
            this.currentPage = page;
          })
          .catch(err => console.error('Greška pri dohvatanju projekata:', err));
    },
    goToNextPage() {
        if (this.nextPage) {
            this.fetchProjects(this.currentPage + 1);
        }
    },
    goToPrevPage() {
        if (this.prevPage) {
            this.fetchProjects(this.currentPage - 1);
        }
    },
    closeModal() {
      this.activeModal = null;
    },
    submitForm(formName, url) {
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
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCsrfToken()
        },
        body: JSON.stringify(payload)
      })
        .then(res => {
          if (!res.ok) throw new Error("Greška pri slanju forme");
          return res.json();
        })
        .then(responseData => {
//          console.log(`Uspešan submit forme "${formName}"`, responseData);
          this.fetchProjects();
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
  },
  watch: {
      searchQuery: {
        handler: function (val) {
          clearTimeout(this._searchTimeout);
          this._searchTimeout = setTimeout(() => {
            this.fetchProjects(); // poziv API-ja sa novim upitom
          }, 700); // čekaj 300ms pre slanja
        },
        immediate: false
      }
  }
})

app.config.compilerOptions.delimiters = ['[[', ']]'];
app.mount('#app');