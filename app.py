
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import time

# ==========================================
# PROFESSIONAL SOCIAL NETWORK DASHBOARD THEME
# ==========================================

import streamlit as st

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #101827 0%,
        #17243A 50%,
        #101827 100%
    );
    color: #F1F5F9;
}

/* Main Content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #1B2940,
        #111C2E
    );
    border-right: 1px solid #334155;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

/* Headings */
h1, h2, h3 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
}

/* Paragraph */
p, label {
    color: #CBD5E1;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #1E314B,
        #17263B
    );
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #334B68;
    box-shadow: 0 5px 18px rgba(0,0,0,0.18);
    transition: 0.3s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #14B8A6;
    transform: translateY(-3px);
}

/* Metric Values */
[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(
        90deg,
        #0D9488,
        #14B8A6
    );
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #0F766E,
        #0D9488
    );
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(20,184,166,0.25);
}

/* Input Fields */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #1E314B !important;
    color: white !important;
    border: 1px solid #475569 !important;
    border-radius: 9px !important;
}

/* Input Focus */
.stTextInput input:focus {
    border-color: #14B8A6 !important;
    box-shadow: 0 0 0 2px rgba(20,184,166,0.2);
}

/* Expanders */
[data-testid="stExpander"] {
    background: #1B2940;
    border: 1px solid #334B68;
    border-radius: 12px;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #334B68;
    border-radius: 10px;
}

/* Info Messages */
.stAlert {
    background: #1E314B;
    border: 1px solid #3B82F6;
    border-radius: 10px;
}

/* Horizontal Divider */
hr {
    border-color: #334B68 !important;
}

/* Graph Container */
[data-testid="stPlotlyChart"] {
    background: #17263B;
    padding: 12px;
    border-radius: 14px;
    border: 1px solid #334B68;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #14B8A6;
    border-radius: 10px;
}

::-webkit-scrollbar-track {
    background: #101827;
}

</style>
""", unsafe_allow_html=True)


# ---------- PAGE CONFIG ----------

st.set_page_config(
    page_title="Social Network Analysis",
    page_icon="🌐",
    layout="wide"
)

# ---------- SESSION STATE ----------

if "G" not in st.session_state:
    st.session_state.G = nx.Graph()

if "result" not in st.session_state:
    st.session_state.result = None

G = st.session_state.G

# ---------- BFS ALGORITHM ----------

def bfs_steps(graph, start):
    visited = {start}
    queue = [start]
    order = []
    steps = []

    while queue:
        node = queue.pop(0)
        order.append(node)

        steps.append({
            "Step": len(steps) + 1,
            "Current User": str(node),
            "Visited Users": ", ".join(map(str, order))
        })

        for neighbor in sorted(graph.neighbors(node)):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order, steps


# ---------- DFS ALGORITHM ----------

def dfs_steps(graph, start):
    visited = set()
    order = []
    steps = []

    def visit(node):
        visited.add(node)
        order.append(node)

        steps.append({
            "Step": len(steps) + 1,
            "Current User": str(node),
            "Visited Users": ", ".join(map(str, order))
        })

        for neighbor in sorted(graph.neighbors(node)):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)

    return order, steps


# ---------- EXECUTION TIME ----------

def measure_time(function, graph, start, repeats=100):
    begin = time.perf_counter()

    for _ in range(repeats):
        function(graph, start)

    return (time.perf_counter() - begin) * 1000 / repeats


# ---------- SIDEBAR ----------

st.sidebar.title("🌐 Social Network")

st.sidebar.subheader("Add Users")

new_user = st.sidebar.text_input("Enter User Name")

if st.sidebar.button("Add User", use_container_width=True):
    name = new_user.strip()

    if name and name not in G:
        G.add_node(name)
        st.sidebar.success("User Added!")
        st.rerun()

    elif name in G:
        st.sidebar.warning("User already exists.")

    else:
        st.sidebar.warning("Enter a user name.")

st.sidebar.divider()
st.sidebar.subheader("Connect Friends")

users = sorted(G.nodes(), key=str)

if len(users) >= 2:

    first = st.sidebar.selectbox(
        "First User", users, key="first"
    )

    second = st.sidebar.selectbox(
        "Second User", users, index=1, key="second"
    )

    if st.sidebar.button("Add Connection", use_container_width=True):

        if first != second and not G.has_edge(first, second):
            G.add_edge(first, second)
            st.sidebar.success("Connection Added!")
            st.rerun()

        elif first == second:
            st.sidebar.error("Select different users.")

        else:
            st.sidebar.warning("Connection already exists.")

else:
    st.sidebar.info("Add at least two users.")

st.sidebar.divider()

# ---------- SAMPLE GRAPH ----------

if st.sidebar.button("Generate Sample Graph", use_container_width=True):

    G.clear()

    sample_users = [
        "Alok", "Rahul", "Aman", "Priya",
        "Neha", "Vishal", "Vikash", "Panu"
    ]

    sample_connections = [
        ("Alok", "Rahul"),
        ("Alok", "Aman"),
        ("Rahul", "Priya"),
        ("Aman", "Priya"),
        ("Priya", "Neha"),
        ("Neha", "Vishal"),
        ("Vishal", "Vikash"),
        ("Vikash", "Panu"),
        ("Panu", "Alok")
    ]

    G.add_nodes_from(sample_users)
    G.add_edges_from(sample_connections)

    st.session_state.result = None
    st.sidebar.success("Sample Graph Created!")
    st.rerun()

if st.sidebar.button("Clear Network", use_container_width=True):
    G.clear()
    st.session_state.result = None
    st.rerun()


# ---------- DASHBOARD ----------

st.title("🌐 Social Network Connection Analysis")

st.caption("Advanced Graph Algorithms and Network Analytics")

total_users = G.number_of_nodes()
total_edges = G.number_of_edges()

density = nx.density(G) if total_users > 1 else 0

avg_friends = (
    sum(dict(G.degree()).values()) / total_users
    if total_users else 0
)

st.subheader("📊 Dashboard Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Users", total_users)
c2.metric("Connections", total_edges)
c3.metric("Network Density", f"{density:.2%}")
c4.metric("Average Friends", f"{avg_friends:.2f}")

st.divider()


# ---------- GRAPH VISUALIZATION ----------

st.subheader("🕸️ Network Visualization")

if total_users > 0:

    fig, ax = plt.subplots(figsize=(12, 7))

    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color="gray",
        width=2
    )

    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color="#69C5E8",
        node_size=1800,
        edgecolors="#0284C7"
    )

    nx.draw_networkx_labels(
        G, pos, ax=ax,
        font_size=10,
        font_weight="bold",
        font_color="black"
    )

    ax.axis("off")

    st.pyplot(fig)
    plt.close(fig)

    st.write("### Graph Information")

    a, b, c = st.columns(3)

    a.metric("Users", total_users)
    b.metric("Connections", total_edges)

    c.metric(
        "Connected Components",
        nx.number_connected_components(G)
    )

else:
    st.info("Add users to generate graph.")

st.divider()


# ---------- BFS AND DFS ----------

st.subheader("🔍 Graph Algorithms - BFS & DFS")

if total_users > 0:

    start = st.selectbox(
        "Select Starting User",
        users,
        key="algorithm_start"
    )

    col1, col2 = st.columns(2)

    if col1.button("▶ Run BFS", use_container_width=True):

        order, steps = bfs_steps(G, start)

        st.session_state.result = {
            "algorithm": "BFS",
            "order": order,
            "steps": steps
        }

    if col2.button("▶ Run DFS", use_container_width=True):

        order, steps = dfs_steps(G, start)

        st.session_state.result = {
            "algorithm": "DFS",
            "order": order,
            "steps": steps
        }

    result = st.session_state.result

    if result:

        st.success(
            result["algorithm"] + ": " +
            " → ".join(map(str, result["order"]))
        )

        st.subheader("Step-by-Step Visualization")

        st.dataframe(
            pd.DataFrame(result["steps"]),
            use_container_width=True,
            hide_index=True
        )

st.divider()


# ---------- SHORTEST PATH ----------

st.subheader("📍 Shortest Connection Path")

if total_users >= 2:

    col1, col2 = st.columns(2)

    source = col1.selectbox(
        "From User", users, key="source"
    )

    destination = col2.selectbox(
        "To User", users, key="destination"
    )

    if st.button("Find Shortest Path"):

        if source == destination:
            st.info("Both users are the same.")

        else:
            try:
                path = nx.shortest_path(
                    G, source, destination
                )

                st.success(" → ".join(map(str, path)))

                st.metric(
                    "Total Connections",
                    len(path) - 1
                )

            except nx.NetworkXNoPath:
                st.warning("No connection path found.")


# ---------- MUTUAL FRIENDS ----------

st.divider()
st.subheader("👥 Mutual Friends")

if total_users >= 2:

    col1, col2 = st.columns(2)

    u1 = col1.selectbox(
        "User 1", users, key="mutual1"
    )

    u2 = col2.selectbox(
        "User 2", users, key="mutual2"
    )

    if st.button("Find Mutual Friends"):

        if u1 != u2:

            common = list(nx.common_neighbors(G, u1, u2))

            if common:
                st.success(", ".join(map(str, common)))
            else:
                st.info("No mutual friends found.")

        else:
            st.warning("Select different users.")


# ---------- BFS VS DFS TIME ----------

st.divider()
st.subheader("⚡ BFS vs DFS Execution Time")

if total_users > 0:

    bfs_time = measure_time(
        bfs_steps, G, users[0]
    )

    dfs_time = measure_time(
        dfs_steps, G, users[0]
    )

    timing_data = pd.DataFrame({
        "Algorithm": ["BFS", "DFS"],
        "Execution Time (ms)": [
            bfs_time, dfs_time
        ]
    })

    st.bar_chart(
        timing_data.set_index("Algorithm")
    )

    st.dataframe(
        timing_data,
        use_container_width=True,
        hide_index=True
    )

    st.caption("Average time calculated over 100 runs.")


# ---------- GRAPH SIZE BENCHMARK ----------

st.divider()
st.subheader("📈 Graph Size Performance Analysis")

if st.button("Run Graph Size Benchmark"):

    benchmark = []

    with st.spinner("Testing graph sizes..."):

        for size in [10, 50, 100, 500]:

            test_graph = nx.gnp_random_graph(
                size,
                min(0.15, 4 / (size - 1)),
                seed=42
            )

            bfs_ms = measure_time(
                bfs_steps,
                test_graph,
                0,
                20
            )

            dfs_ms = measure_time(
                dfs_steps,
                test_graph,
                0,
                20
            )

            benchmark.append({
                "Users": size,
                "BFS Time (ms)": bfs_ms,
                "DFS Time (ms)": dfs_ms
            })

    st.session_state.benchmark = benchmark

if "benchmark" in st.session_state:

    df = pd.DataFrame(st.session_state.benchmark)

    st.line_chart(
        df.set_index("Users")
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.caption(
    "DAA Project 4 | Social Network Connection and Recommendation Analysis"
)
