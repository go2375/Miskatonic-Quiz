import pandas as pd
import re


QUESTIONS_PATH = "./data/questions.csv"


def etl_quiz(csv_path: str = QUESTIONS_PATH) -> pd.DataFrame:
   

    # EXTRACT : charger le CSV
    df = pd.read_csv(csv_path)
    print(f"✅ Fichier chargé : {csv_path} ({len(df)} lignes)")

    

    # 3) Repérer les colonnes des réponses (responseA, responseB, ...)
    response_cols = [c for c in df.columns if c.lower().startswith("response")]

    # 4) Construire la liste des réponses présentes pour chaque ligne
    #    - on enlève les NaN
    #    - on strip les espaces
    df["all_responses"] = df[response_cols].apply(
        lambda row: [str(x).strip() for x in row if pd.notna(x) and str(x).strip() != ""],
        axis=1,
    )

    # enlever les deux-points
    if "question" in df.columns:
        df["question"] = df["question"].astype(str).str.replace(":", "", regex=False).str.strip()

    # Petite fonction utilitaire : extraire les lettres correctes (A, B, C, D)
      
    def split_correct_letters(value) -> list[str]:
        if pd.isna(value):
            return []
        s = str(value).upper().strip()
        # remplace séparateurs divers par espaces (virgule, point-virgule, /, etc.)
        s = re.sub(r"[^\w]", " ", s)
        # ne garder que A, B, C, D
        return re.findall(r"[ABCD]", s)

 #Extraire le texte des bonnes réponses pour chaque ligne
    def get_correct_responses(row) -> list[str]:
        letters = split_correct_letters(row.get("correct"))
        results = []
        for letter in letters:
            colname = f"response{letter}"
            if colname in row and pd.notna(row[colname]) and str(row[colname]).strip():
                results.append(str(row[colname]).strip())
        return results

    df["correct_responses"] = df.apply(get_correct_responses, axis=1)

    # Filtrer les lignes invalides :
    #    - question non vide
    #    - au moins une réponse
    #    - au moins une bonne réponse
    df = df[df["question"].notna()]
    df = df[df["question"].str.strip() != ""]
    df = df[df["all_responses"].map(len) > 0]
    df = df[df["correct_responses"].map(len) > 0]

    # re-nettoyer les listes au cas où
    df["all_responses"] = df["all_responses"].apply(
        lambda lst: [r for r in lst if str(r).strip() != ""]
    )
    df["correct_responses"] = df["correct_responses"].apply(
        lambda lst: [r for r in lst if str(r).strip() != ""]
    )

    #  GROUP BY question : fusionner les réponses et bonnes réponses
    #     - on utilise un set pour éviter les doublons
    cols_to_keep = ["subject"] if "subject" in df.columns else []
    grouped = (
        df.groupby("question", as_index=False)
          .agg({
              **{c: "first" for c in cols_to_keep},
              "all_responses": lambda x: list({resp for sub in x for resp in sub}),
              "correct_responses": lambda x: list({resp for sub in x for resp in sub}),
          })
    )

    # 11) Infos de synthèse
    print(f"Lignes valides après filtrage : {len(grouped)} questions uniques")
    # print(grouped.head(5))  # décommente pour voir un aperçu

    # retourne le DataFrame
    return grouped


if __name__ == "__main__":
    # Exécution simple : retourne le DataFrame transformé et l’affiche
    result = etl_quiz()
    print(result.head(10))  # petit aperçu en console
   

