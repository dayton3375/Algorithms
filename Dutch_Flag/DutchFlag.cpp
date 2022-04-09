#include <iostream>
#include <vector>

using namespace std;

#define NUMBER_OF_BLACK 15
#define NUMBER_OF_BROWN 30

// Helps with making the colors more readable
enum baby
{
    BLACK, BROWN
};

// Creates BLACK babies on left and BROWN on right
void HalfAndHalf(vector<baby> & babySet)
{
    for (int i = 0; i < NUMBER_OF_BLACK; ++i)
    {
        babySet.push_back(BLACK);
    }

    for (int i = 0; i < NUMBER_OF_BROWN; ++i)
    {
        babySet.push_back(BROWN);
    }
}

// Swaps the baby colors at the indexes pointed to
void SwapBabies(baby * p0, baby * p1)
{
    baby buffBaby = *p0;
    *p0 = *p1;
    *p1 = buffBaby;
}

// Sorts babies so they are alternating BLACK and BROWN
void SortEveryOther(vector<baby> & babySet)
{
    baby *p0 = nullptr;
    baby *p1 = nullptr;
    int i = 0;
    int j = 1;
    // Sort the vector of babies alternating
    while (j < babySet.size())
    {
        p0 = &babySet[i];
        p1 = &babySet[j];

        switch(*p1)
        {
            case BLACK:
                break;
            case BROWN:
                // swap and increment each by 2
                SwapBabies(p0, p1);
                i += 2, ++j; // (increment by 2) will increment j at end of loop
                break;
            default:
                cout << "[ERROR in sorting - wrong baby type at index " << j << "]" << endl;
                break;            
        }
        
        ++j;
    }
}

// Sorts babies in BLACK BROWN BROWN pattern
void Black2Brown(vector<baby> & babySet)
{
    baby *p0 = nullptr;
    baby *p1 = nullptr;
    baby *p2 = nullptr;

    // start each index so the three pointers are next to each other
    int i = 0;
    int j = 1;
    int k = 2;

    while ((i < babySet.size()) && (j < babySet.size()) && (k < babySet.size()))
    {
        // set pointers at indexes
        p0 = &babySet[i];
        p1 = &babySet[j];
        p2 = &babySet[k];

        switch(*p0)
        {
            case BROWN:
                // swap with the pointer at lowest index
                if (*p1 == BLACK && j < k)
                {
                    // swap and increment
                    SwapBabies(p0, p1);
                    i += 3;
                    j += 3;
                    p0 = &babySet[i];
                    p1 = &babySet[j];
                }
                else if (*p2 == BLACK && k < j)
                {
                    // swap and increment
                    SwapBabies(p0, p2);
                    i += 3;
                    k += 3;
                    p0 = &babySet[i];
                    p2 = &babySet[k];
                }
                else
                {
                    cout << "[ERROR code 1 in sorting, likely j == k]";
                }
                break;
            case BLACK:
                // GOOD so increment
                i += 3;
                p0 = &babySet[i];
                break;
            default:
                cout << "[ERROR code 2 in sorting - wrong baby type]" << endl;
                return;            
        }

        switch (*p1)
        {
            case BROWN:
                // GOOD so increment
                j += 3;
                p1 = &babySet[j];
                break;
            case BLACK:
                if (*p0 == BROWN)
                {
                    // swap and increment
                    SwapBabies(p0, p1);
                    i += 3;
                    j += 3;
                    p0 = &babySet[i];
                    p1 = &babySet[j];
                }
                break;
            default:
                cout << "[ERROR code 3 in sorting - wrong baby type]" << endl;
                return;            
        }

        switch (*p2)
        {
            case BROWN:
                // GOOD so increment
                k += 3;
                p2 = &babySet[k];
                break;
            case BLACK:
                if (*p0 == BROWN)
                {
                    // swap and increment
                    SwapBabies(p0, p2);
                    i += 3;
                    k += 3;
                    p0 = &babySet[i];
                    p2 = &babySet[k];
                }
                break;
            default:
                cout << "[ERROR code 4 in sorting - wrong baby type]" << endl;
                return;            
        }
    }
}

void PrintBabies(vector<baby> & babySet)
{
    // prints the babies
    for (int i = 0; i < babySet.size(); ++i)
    {
        switch(babySet[i])
        {
            case BLACK:
                cout << "BLACK " << endl;
                break;
            case BROWN:
                cout << "BROWN " << endl;
                break;
            default:
                cout << "ERROR" << endl;
                break;
        }
    }
}

int main(void)
{
    // the set of babies (initialized empty)
    vector<baby> babySet;

    HalfAndHalf(babySet);
    Black2Brown(babySet);
    PrintBabies(babySet);

    return 0;
}