from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import pandas as pd

# ✅ Load and format dataset
df = pd.read_excel("./Final Cricket Dataset.xlsx")

docs = []
for _, row in df.iterrows():
    info = f"""
    {row['Name']} from {row['Place']} scored {row['International Runs']} international runs including {row['ODI Runs']} ODI runs, {row['Test Runs']} Test runs, and {row['T20 Runs']} T20 runs.
    His highest score was {row['Maximum Score']}.
    He last played at {row['Last Match Venue']} on {row['Last Match Date']} and scored {row['Runs in Last Match']} runs in that match.
    """
    docs.append(info.strip())

# ✅ Use smaller model to reduce deployment size
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_texts(docs, embedding)

model_name = "google/flan-t5-small"  # 👈 Smaller model (~100MB vs 1.2GB)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

qa_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=256)
llm = HuggingFacePipeline(pipeline=qa_pipeline)

prompt_template = PromptTemplate.from_template("""
You are CrickChat, a helpful and friendly cricket assistant. Use the context to answer the user's question clearly and conversationally. Answer only based on the player the user is asking about. Don't add unrelated players or extra stats.

Context:
{context}

Question: {question}

Answer as a friendly chatbot:
""")

retriever = db.as_retriever(search_kwargs={"k": 1})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt_template}
)

def ask_crickchat(query: str) -> str:
    return qa_chain.run(query)
