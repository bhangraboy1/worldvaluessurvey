# This is a sample Python script.
import pandas as pd
import matplotlib.pyplot as plt
import math

#Global Definitions
states = ['Bihar', 'Delhi', 'Haryana', 'Maharashtra', 'Punjab',
          'Telangana', 'Uttar Pradesh', 'West Bengal']
answers     = [[0.0 for y in range(50)] for s in states]
answers_top = [[0.0 for y in range(50)] for s in states]
expected_values = [-1, 1, 2, 3, 4]
values = [0, +2, +1, -1, -2]
full_color_map = {
    -1: 'lightgray',  # Don't Know / No Answer
    1: '#1b9e77',  # Bold Green (Strongly Agree)
    2: '#d95f02',  # Bold Orange (Agree)
    3: '#7570b3',  # Bold Purple (Disagree)
    4: '#e7298a',  # Bold Pink (Strongly Disagree)
    5: '#e7298a'
}
label_map = {
    -1: "Missing",
    1: "Strongly Agree",
    2: "Agree",
    3: "Disagree",
    4: "Strongly Disagree"
}
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def get_data():
    iso_to_state = {
        356004: 'Bihar',
        356008: 'Haryana',
        356015: 'Maharashtra',
        356021: 'Punjab',
        356025: 'Telangana',
        356028: 'Uttar Pradesh',
        356029: 'West Bengal',
        356034: 'Delhi'
    }
    ms_to_marital = {
        1: 'Married',
        2: 'Living Together',
        3: 'Divorced',
        4: 'Separated',
        5: 'Widowed',
        6: 'Single'
    }
    code_to_gender = {
        1:  'Male',
        2:  'Female'
    }
    code_to_lang =  {
        490:    'Bengali',
        1740:   'Hindi',
        2940:   'Marathi',
        3540:   'Punjabi',
        4220:   'Telegu',
        9000:   'Other',
        -1:     'Missing'
    }
    code_to_religion = {
        -1: 'Missing',
        1:  'Roman Catholic',
        5:  'Muslim',
        6:  'Hindu',
        7:  'Buddhist',
        9:  'Other'
    }
    code_to_caste = {
        356017:  'SC',
        356018:  'ST',
        356019:  'OBC',
        356024:  'General'
    }
    df = pd.read_csv('WVS_Cross-National_Wave_7_csv_v6_0.csv')
#    print(df.loc[0])
    print("Size")
    print(df.shape)

    dg = pd.DataFrame()
    dg = df[df['C_COW_ALPHA'] == 'IND'].copy()
    dg['STATE_NAME'] = dg['N_REGION_ISO'].map(iso_to_state)
    dg['MARITAL_STATUS'] = dg['Q273'].map(ms_to_marital)
    dg['LANGUAGE'] = dg['Q272'].map(code_to_lang)
    dg['RELIGION'] = dg['Q289'].map(code_to_religion)
    dg['CASTE'] = dg['Q290'].map(code_to_caste)
    dg['GENDER'] = dg['Q260'].map(code_to_gender)

    print("Filtered Size")
    print(dg.shape)

    i = 0
    print(dg['C_COW_ALPHA'].iloc[i], dg['A_YEAR'].iloc[i], dg['A_WAVE'].iloc[i],
          dg['O1_LONGITUDE'].iloc[i], dg['O2_LATITUDE'].iloc[i], dg['N_REGION_ISO'].iloc[i],
          dg['W_WEIGHT'])

    print(dg)
    return (dg)

def graph(dg):
    fig, axs = plt.subplots(3,3, figsize=(15,10))
    fig.suptitle('Demographic Data - World Values Survey - Wave 7')
    demographics    = ['STATE_NAME', 'GENDER', 'Q275', 'MARITAL_STATUS',
                       'RELIGION', 'CASTE', 'Q274', 'LANGUAGE']
    xlabel          = ['States', 'Gender', 'Education', 'Marital Status',
                       'Religion', 'Caste', 'Children', 'Language']
    title           = ['Responses by State', 'Gender', 'Education', 'Marital Status',
                       'Religion', 'Caste', 'Children', 'Language']
    sort            = [False, False, True, False, False, False, True, False]

    for x in range(3):
        for y in range(3):
            index = 3 * x + y
            if (index < len(demographics)):
                if (sort[index]):
                    counts = dg[demographics[index]].value_counts().sort_index()
                else:
                    counts = dg[demographics[index]].value_counts()
                counts.plot(kind='bar', ax=axs[x, y])
                axs[x, y].set_title(title[index])
                axs[x, y].set_xlabel(xlabel[index])
                axs[x, y].set_ylabel("Frequency")
                axs[x, y].tick_params(axis='x', labelrotation=45)

    plt.tight_layout()
    plt.savefig("demographics.pdf")
    plt.show()

def graph_economics(dg):
    maxrow=2; maxcol=3; offset=5
    fig, axs = plt.subplots(maxrow, maxcol, figsize=(15,10))
    fig.suptitle('State-Wide Social Norm Index - Economics - Wave 7 - Sorted')
    demographics    = ['Q32', 'Q33', 'Q35']
    xlabel          = ['Being a Housewife', 'Jobs are Scarce', 'Women Earning More']
    title           = ['Being a Housewife as Fullfilling as Working for Pay',
                       'Jobs are Scarce, men Should have Priority',
                       'Women Earning More Causes Problems']
    sort            = [True, False, False]

    for x in range(1):
        for y in range(3):
            index = 3 * x + y
            if (index < len(demographics)):
                categorical_data = pd.Categorical(dg[demographics[index]], categories=expected_values)
                if (sort[index]):
                    counts = pd.crosstab(dg['STATE_NAME'], categorical_data, aggfunc='sum',  normalize='index', values=dg['W_WEIGHT'], dropna=False)
                else:
                    counts = pd.crosstab(dg['STATE_NAME'], categorical_data, aggfunc='sum',  normalize='index', values=dg['W_WEIGHT'], dropna=False)
                current_colors = [full_color_map[col] for col in counts.columns]

#                pos_cols = [c for c in [1,2] if c in counts.columns]
#                counts['sort_val'] = counts[pos_cols].sum(axis=1)
#                counts = counts.sort_values(by='sort_val', ascending=False).drop(columns=['sort_val'])

                counts = counts.rename(columns=label_map)
                counts.plot(kind='bar', stacked=True, ax=axs[x, y], color=current_colors)
                axs[x, y].set_title(title[index])
                axs[x, y].set_xlabel(xlabel[index])
                axs[x, y].set_ylabel("Percentage (%)")
                axs[x,y].set_ylim(0,1)
                axs[x, y].tick_params(axis='x', labelrotation=45)
                s = 0
                while (s < len(states)):
                    total  = 0.0
                    totalv = 0.0
#                    print('In Economics', states[s])
                    for l in range(1, 5, 1):
                        totalv = totalv + counts[label_map[l]][states[s]] * values[l]
                        total  = total  + counts[label_map[l]][states[s]]
                    answers[s][index+offset] = (totalv / total)
                    answers_top[s][index+offset] = counts[label_map[1]][states[s]] / total
                    s += 1
            else:
                axs[x, y].axis('off')
# Creating an Average SSNI - Economic Index
    avg_df = dg.melt(id_vars=['STATE_NAME'], value_vars=demographics, value_name='response')
    avg_df = avg_df[avg_df['response'] > 0]  # Filter invalid responses
    avg_counts = pd.crosstab(avg_df['STATE_NAME'], avg_df['response'], normalize='index')
    current_colors = [full_color_map[col] for col in avg_counts.columns]

    # Sort by aggregate Positive Sentiment
    pos_cols_avg = [c for c in [1, 2] if c in avg_counts.columns]
    avg_counts['sort_val'] = avg_counts[pos_cols_avg].sum(axis=1)
    avg_counts = avg_counts.sort_values(by='sort_val', ascending=False).drop(columns=['sort_val'])

    a = (((len(demographics)-1) % maxcol) + 1) % maxcol
    b = math.floor(((len(demographics)+1) / maxcol))
    print ("Row", b, "Column", a)

    # Plot in the first slot of the second row
    avg_counts = avg_counts.rename(columns=label_map)
    avg_counts.plot(kind='bar', stacked=True, ax=axs[b, a], color=current_colors)
#    , color = plt.cm.Paired.colors



    axs[b, a].set_title("SSNI - Economic (Average of 3 Questions)", fontweight='bold')
    axs[b, a].set_ylim(0, 1)
    axs[b, a].tick_params(axis='x', labelrotation=45)
    for label in axs[b, a].get_xticklabels():
        label.set_horizontalalignment('right')

    plt.tight_layout()
    plt.savefig("economics.pdf")
    plt.show()

def graph_political(dg):
    maxrow=2; maxcol=3
    fig, axs = plt.subplots(maxrow, maxcol, figsize=(15,10))
    fig.suptitle('State-Wide Social Norm Index - Political - Wave 7 - Sorted')
    demographics    = ['Q29', 'Q209', 'Q210', 'Q211', 'Q212']
    xlabel          = ['Poltical Leaders', 'Signing a Petition', 'Joining in Boycotts',
                       'Attending Demonstrations', 'Joining Strikes']
    title           = ['Men Make Better Political Leaders', 'Signing a Petition',
                       'Attending Demonstrations', 'Joining in Boycotts', 'Joining Strikes']
    sort            = [False, False, False, False, False]

    for x in range(2):
        for y in range(3):
# For each question
            index = 3 * x + y
            if (index < len(demographics)):
                categorical_data = pd.Categorical(dg[demographics[index]], categories=expected_values)
                if (sort[index]):
                    counts = pd.crosstab(dg['STATE_NAME'], categorical_data, aggfunc='sum',  normalize='index', values=dg['W_WEIGHT'], dropna=False)
                else:
                    counts = pd.crosstab(dg['STATE_NAME'], categorical_data, aggfunc='sum',  normalize='index', values=dg['W_WEIGHT'], dropna=False)

                current_colors = [full_color_map[col] for col in counts.columns]
                counts = counts.rename(columns=label_map)
                counts.plot(kind='bar', stacked=True, ax=axs[x, y], color=current_colors)
                axs[x, y].set_title(title[index])
                axs[x, y].set_xlabel(xlabel[index])
                axs[x, y].set_ylabel("Percentage (%)")
                axs[x, y].set_ylim(0, 1)
                axs[x, y].tick_params(axis='x', labelrotation=45)

                s = 0
                while (s < len(states)):
                    total  = 0.0
                    totalv = 0.0
                    for l in range(1, 5, 1):
                        totalv = totalv + counts[label_map[l]][states[s]] * values[l]
                        total  = total  + counts[label_map[l]][states[s]]
                    answers[s][index] = (totalv / total)
                    answers_top[s][index] = counts[label_map[1]][states[s]] / total

                    s += 1
#                pos_cols = [c for c in [1,2] if c in counts.columns]
#                counts['sort_val'] = counts[pos_cols].sum(axis=1)
#                counts = counts.sort_values(by='sort_val', ascending=False).drop(columns=['sort_val'])

# Averaging Across All Questions
        avg_df = dg.melt(id_vars=['STATE_NAME'], value_vars=demographics, value_name='response')
        avg_df = avg_df[avg_df['response'] > 0]  # Filter invalid responses
        avg_counts = pd.crosstab(avg_df['STATE_NAME'], avg_df['response'], normalize='index')
        current_colors = [full_color_map[col] for col in avg_counts.columns]

        a = (((len(demographics) - 1) % maxcol) + 1) % maxcol
        b = math.floor(((len(demographics) + 1) / maxcol)) - 1

        # Sort by aggregate Positive Sentiment
        pos_cols_avg = [c for c in [1, 2] if c in avg_counts.columns]
        avg_counts['sort_val'] = avg_counts[pos_cols_avg].sum(axis=1)
        avg_counts = avg_counts.sort_values(by='sort_val', ascending=False).drop(columns=['sort_val'])

        # Plot in the first slot of the second row
        avg_counts = avg_counts.rename(columns=label_map)
        avg_counts.plot(kind='bar', stacked=True, ax=axs[b, a], color=current_colors)

        axs[b, a].set_title("SSNI - Political (Average of 3 Questions)", fontweight='bold')
        axs[b, a].set_ylim(0, 1)
        axs[b, a].tick_params(axis='x', labelrotation=45)
        for label in axs[b, a].get_xticklabels():
            label.set_horizontalalignment('right')

    plt.tight_layout()
    plt.savefig("political.pdf")
    plt.show()


def graph_violence(dg):
    maxrow=2; maxcol=3; offset=8
    fig, axs = plt.subplots(maxrow, maxcol, figsize=(15,10))
    fig.suptitle('State-Wide Social Norm Index - Violence - Wave 7 - Sorted')
    demographics    = ['Q189', 'Q191', 'Q137']
    xlabel          = ['Man to Beat His Wife', 'Violence Against Others', 'Street Violence']
    title           = ['Man to Beat His Wife', 'Violence Against Others', 'Street Violence']
    sort            = [False, False, False]
    full_color_map = {
        -1: 'lightgray',      # Don't Know / No Answer
         1: '#1b9e77',        # Bold Green (Strongly Agree)
         2: '#d95f02',        # Bold Orange (Agree)
         3: '#7570b3',        # Bold Purple (Disagree)
         4: '#e7298a',         # Bold Pink (Strongly Disagree)
         5: '#e7299a',
         6: '#e729aa',
         7: '#e729ba',
         8: '#e729ca',
         9: '#e729da',
        10: '#e729ea'
    }

    for x in range(3):
        for y in range(3):
            index = 3 * x + y
            if (index < len(demographics)):
                categorical_data = pd.Categorical(dg[demographics[index]], categories=expected_values)
                if (sort[index]):
                    counts = pd.crosstab(dg['STATE_NAME'], categorical_data, aggfunc='sum',  normalize='index', values=dg['W_WEIGHT'], dropna=False)
                else:
                    counts = pd.crosstab(dg['STATE_NAME'], categorical_data, aggfunc='sum',  normalize='index', values=dg['W_WEIGHT'], dropna=False)

                current_colors = [full_color_map[col] for col in counts.columns]

#                pos_cols = [c for c in [1,2] if c in counts.columns]
#                counts['sort_val'] = counts[pos_cols].sum(axis=1)
#                counts = counts.sort_values(by='sort_val', ascending=False).drop(columns=['sort_val'])

                counts = counts.rename(columns=label_map)
                counts.plot(kind='bar', stacked=True, ax=axs[x, y], color=current_colors, legend=False)
                axs[x, y].set_title(title[index])
                axs[x, y].set_xlabel(xlabel[index])
                axs[x, y].set_ylabel("Percentage (%)")
                axs[x, y].set_ylim(0,1)
                axs[x, y].tick_params(axis='x', labelrotation=45)

                s = 0
                while (s < len(states)):
                    total  = 0.0
                    totalv = 0.0
                    for l in range(1, 5, 1):
#                        print('Violence', s, l, index, counts[label_map[l]][states[s]])
                        totalv = totalv + counts[label_map[l]][states[s]] * values[l]
                        total  = total  + counts[label_map[l]][states[s]]
                    answers[s][index+offset] = (totalv / total)
                    answers_top[s][index+offset] = counts[label_map[1]][states[s]] / total

                    s += 1

    avg_df = dg.melt(id_vars=['STATE_NAME'], value_vars=demographics, value_name='response')
    avg_df = avg_df[avg_df['response'] > 0]  # Filter invalid responses
    avg_counts = pd.crosstab(avg_df['STATE_NAME'], avg_df['response'], normalize='index')
    current_colors = [full_color_map[col] for col in avg_counts.columns]

    a = (((len(demographics) - 1) % maxcol) + 1) % maxcol
    b = math.floor(((len(demographics) + 1) / maxcol))

    print("Row", b, "Column", a)

        # Sort by aggregate Positive Sentiment
    pos_cols_avg = [c for c in [1, 2] if c in avg_counts.columns]
    avg_counts['sort_val'] = avg_counts[pos_cols_avg].sum(axis=1)
    avg_counts = avg_counts.sort_values(by='sort_val', ascending=False).drop(columns=['sort_val'])

        # Plot in the first slot of the second row
    avg_counts = avg_counts.rename(columns=label_map)
    avg_counts.plot(kind='bar', stacked=True, ax=axs[b, a], color=current_colors, legend=True)

    axs[b, a].set_title("SSNI - Violence (Average of 3 Questions)", fontweight='bold')
    axs[b, a].set_ylim(0, 1)
    axs[b, a].tick_params(axis='x', labelrotation=45)
    for label in axs[b, a].get_xticklabels():
        label.set_horizontalalignment('right')

    plt.tight_layout()
    plt.savefig("violence.pdf")
    plt.show()

def graph_education(dg):
    maxrow=2; maxcol=2; offset=11
    fig, axs = plt.subplots(maxrow, maxcol, figsize=(15,10))
    fig.suptitle('State-Wide Social Norm Index - Violence - Wave 7 - Sorted')
    demographics    = ['Q30']
    xlabel          = ['University Education']
    title           = ['University Education']
    sort            = [False]
    full_color_map = {
        -1: 'lightgray',      # Don't Know / No Answer
         1: '#1b9e77',        # Bold Green (Strongly Agree)
         2: '#d95f02',        # Bold Orange (Agree)
         3: '#7570b3',        # Bold Purple (Disagree)
         4: '#e7298a',         # Bold Pink (Strongly Disagree)
         5: '#e7299a',
         6: '#e729aa',
         7: '#e729ba',
         8: '#e729ca',
         9: '#e729da',
        10: '#e729ea'
    }

    for x in range(2):
        for y in range(2):
            index = 3 * x + y
            if (index < len(demographics)):
                categorical_data = pd.Categorical(dg[demographics[index]], categories=expected_values)
                if (sort[index]):
                    counts = pd.crosstab(dg['STATE_NAME'], categorical_data, aggfunc='sum',  normalize='index', values=dg['W_WEIGHT'], dropna=False)
                else:
                    counts = pd.crosstab(dg['STATE_NAME'], categorical_data, aggfunc='sum',  normalize='index', values=dg['W_WEIGHT'], dropna=False)

                current_colors = [full_color_map[col] for col in counts.columns]

#                pos_cols = [c for c in [1,2] if c in counts.columns]
#                counts['sort_val'] = counts[pos_cols].sum(axis=1)
#                counts = counts.sort_values(by='sort_val', ascending=False).drop(columns=['sort_val'])

                counts = counts.rename(columns=label_map)
                counts.plot(kind='bar', stacked=True, ax=axs[x, y], color=current_colors, legend=False)
                axs[x, y].set_title(title[index])
                axs[x, y].set_xlabel(xlabel[index])
                axs[x, y].set_ylabel("Percentage (%)")
                axs[x, y].set_ylim(0,1)
                axs[x, y].tick_params(axis='x', labelrotation=45)
                s = 0
                while (s < len(states)):
                    total = 0.0
                    totalv = 0.0
                    for l in range(1, 5, 1):
                        #                        print('Violence', s, l, index, counts[label_map[l]][states[s]])
                        totalv = totalv + counts[label_map[l]][states[s]] * values[l]
                        total = total + counts[label_map[l]][states[s]]
                    answers[s][index + offset] = (totalv / total)
                    answers_top[s][index+offset] = counts[label_map[1]][states[s]] / total

                    s += 1
    avg_df = dg.melt(id_vars=['STATE_NAME'], value_vars=demographics, value_name='response')
    avg_df = avg_df[avg_df['response'] > 0]  # Filter invalid responses
    avg_counts = pd.crosstab(avg_df['STATE_NAME'], avg_df['response'], normalize='index')
    current_colors = [full_color_map[col] for col in avg_counts.columns]

    a = (((len(demographics) - 1) % maxcol) + 1) % maxcol
    b = math.floor(((len(demographics) + 1) / maxcol))

    print("Row", b, "Column", a)

    # Sort by aggregate Positive Sentiment
    pos_cols_avg = [c for c in [1, 2] if c in avg_counts.columns]
    avg_counts['sort_val'] = avg_counts[pos_cols_avg].sum(axis=1)
    avg_counts = avg_counts.sort_values(by='sort_val', ascending=False).drop(columns=['sort_val'])

    # Plot in the first slot of the second row
    avg_counts = avg_counts.rename(columns=label_map)
    avg_counts.plot(kind='bar', stacked=True, ax=axs[b, a], color=current_colors, legend=True)

    axs[b, a].set_title("SSNI - Violence (Average of 3 Questions)", fontweight='bold')
    axs[b, a].set_ylim(0, 1)
    axs[b, a].tick_params(axis='x', labelrotation=45)
    for label in axs[b, a].get_xticklabels():
        label.set_horizontalalignment('right')

    plt.tight_layout()
    plt.savefig("education.pdf")
    plt.show()
#   plt.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

    dg = get_data()
#    graph(dg)
    graph_political(dg)
    graph_economics(dg)
    graph_violence(dg)
    graph_education(dg)

    print("Values Across States for each Question")
    print("Political First (5), Economics(3), Violence(3), Education(1)")
    print("Averages")
    for s in range(8):
        print("%13s" % states[s], end=" ")
        for q in range(5+3+3+1):
            print("%7.3f" % answers[s][q], end=" ")
        print()

    print("Top")
    for s in range(8):
        print("%13s" % states[s], end=" ")
        for q in range(5+3+3+1):
            print("%7.3f" % answers_top[s][q], end=" ")
        print()