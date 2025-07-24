from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import pandas as pd

# ✅ Load your Excel dataset
df = pd.read_excel("./Final Cricket Dataset.xlsx")

# ✅ Create context strings
docs = []
for _, row in df.iterrows():
    info = f"""
    {row['Name']} from {row['Place']} scored {row['International Runs']} international runs including {row['ODI Runs']} ODI runs, {row['Test Runs']} Test runs, and {row['T20 Runs']} T20 runs.
    His highest score was {row['Maximum Score']}.
    He last played at {row['Last Match Venue']} on {row['Last Match Date']} and scored {row['Runs in Last Match']} runs in that match.
    """
    docs.append(info.strip())

# ✅ Embeddings
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ FAISS Vector Store
db = FAISS.from_texts(docs, embedding)

# ✅ Load FLAN-T5 model
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# ✅ Pipeline + LangChain wrapper
qa_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=256)
llm = HuggingFacePipeline(pipeline=qa_pipeline)

# ✅ Prompt template
prompt_template = PromptTemplate.from_template("""
You are CrickChat, a helpful and friendly cricket assistant. Use the context to answer the user's question clearly and conversationally. Answer only based on the player the user is asking about. Don't add unrelated players or extra stats.

Context:
{context}

Question: {question}

Answer as a friendly chatbot:
""")

retriever = db.as_retriever(search_kwargs={"k": 1})

# ✅ Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt_template}
)

# ✅ Function used by FastAPI
def ask_crickchat(query: str) -> str:
    return qa_chain.run(query)
