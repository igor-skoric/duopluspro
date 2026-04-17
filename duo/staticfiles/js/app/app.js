const { createApp } = Vue;

const app = createApp({
  data() {
    return {
      searchQuery: "",
      statusFilter: "",
      projects: [],
      activeModal: null,
      formProject: {
        id: null,
        name: "",
        client: "",
        contact: "",
        start_date: "",
        end_date: null,
        status: "",
        note: "",
      },
      sections: {
        addProject: true,
      },
      nextPage: null,
      prevPage: null,
      totalCount: 0,
      currentPage: 1,
      pageSize: 12,
    };
  },
  computed: {
    hasActiveFilters() {
      return !!(this.searchQuery?.trim() || this.statusFilter);
    },
  },
  mounted() {
    this.fetchProjects(1);
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return "—";
      const date = new Date(dateStr);
      if (isNaN(date)) return "—";
      return date.toLocaleDateString("sr-RS");
    },
    getCsrfToken() {
      const name = "csrftoken";
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const c = cookies[i].trim();
        if (c.startsWith(name + "=")) {
          return decodeURIComponent(c.substring(name.length + 1));
        }
      }
      return "";
    },
    statusClass(status) {
      switch (status) {
        case "planned":
          return "bg-sky-100 text-sky-900 ring-1 ring-sky-200";
        case "active":
          return "bg-emerald-100 text-emerald-900 ring-1 ring-emerald-200";
        case "paused":
          return "bg-amber-100 text-amber-900 ring-1 ring-amber-200";
        case "completed":
          return "bg-stone-200 text-stone-800 ring-1 ring-stone-300";
        case "cancelled":
          return "bg-red-100 text-red-900 ring-1 ring-red-200";
        default:
          return "bg-stone-200 text-stone-800";
      }
    },
    clearFilters() {
      this.searchQuery = "";
      this.statusFilter = "";
      this.fetchProjects(1);
    },
    openModal(section) {
      this.activeModal = section;
    },
    fetchProjects(page = 1) {
      const params = new URLSearchParams();
      params.set("page", String(page));
      params.set("page_size", String(this.pageSize));
      const q = this.searchQuery?.trim();
      if (q) params.set("search", q);
      if (this.statusFilter) params.set("status", this.statusFilter);

      const url = `/construction/api/projects/?${params.toString()}`;

      fetch(url)
        .then((res) => res.json())
        .then((data) => {
          this.projects = data.results || [];
          this.totalCount = data.count;
          this.nextPage = data.next;
          this.prevPage = data.previous;
          this.currentPage = page;
        })
        .catch((err) => console.error("Greška pri dohvatanju projekata:", err));
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

      const payload = { ...form };
      if (!payload.project && this.project?.id) {
        payload.project = this.project.id;
      }

      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.getCsrfToken(),
        },
        body: JSON.stringify(payload),
      })
        .then((res) => {
          if (!res.ok) throw new Error("Greška pri slanju forme");
          return res.json();
        })
        .then(() => {
          this.fetchProjects(this.currentPage);
          this.closeModal();

          for (let key in this[formName]) {
            this[formName][key] = "";
          }
        })
        .catch((error) => {
          console.error(`Greška pri slanju "${formName}":`, error);
        });
    },
  },
  watch: {
    searchQuery: {
      handler() {
        clearTimeout(this._searchTimeout);
        this._searchTimeout = setTimeout(() => {
          this.fetchProjects(1);
        }, 500);
      },
      immediate: false,
    },
    statusFilter() {
      this.fetchProjects(1);
    },
  },
});

app.config.compilerOptions.delimiters = ["[[", "]]"];
app.mount("#app");
