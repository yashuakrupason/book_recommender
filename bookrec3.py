# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:22:28 2019

@author: KRUPASON
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import Combobox








books = pd.read_csv('BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher',
                 'imageUrlS', 'imageUrlM', 'imageUrlL']
users = pd.read_csv('BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
ratings.columns = ['userID', 'ISBN', 'bookRating']

print(ratings.shape)
print(list(ratings.columns))

plt.rc("font", size=15)
ratings.bookRating.value_counts(sort=False).plot(kind='bar')
plt.title('Rating Distribution\n')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.savefig('system1.png', bbox_inches='tight')
plt.show()

print(books.shape)
print(list(books.columns))

print(users.shape)
print(list(users.columns))

users.Age.hist(bins=[0, 10, 20, 30, 40, 50, 100])
plt.title('Age Distribution\n')
plt.xlabel('Age')
plt.ylabel('Count')
plt.savefig('system2.png', bbox_inches='tight')
plt.show()

combine_book_rating = pd.merge(ratings, books, on='ISBN')


columns = ['yearOfPublication', 'publisher', 'bookAuthor', 'imageUrlS', 'imageUrlM', 'imageUrlL']
combine_book_rating = combine_book_rating.drop(columns, axis=1)
combine_book_rating.head()

combine_book_rating = combine_book_rating.dropna(axis = 0, subset = ['bookTitle'])

'''
userid=int(input("Enter User ID"))
bookn=input("Enter bookname")
l=combine_book_rating.loc[(combine_book_rating.bookTitle==bookn)&(combine_book_rating.userID==userid)].index[0]
rating_new=int(input("Enter new Rating"))
combine_book_rating.at[l,'bookRating']=rating_new
l=list(set(list(combine_book_rating['bookTitle'])))
c=combine_book_rating'''

book_ratingCount = (combine_book_rating.
     groupby(by = ['bookTitle'])['bookRating'].
     count().
     reset_index().
     rename(columns = {'bookRating': 'totalRatingCount'})
     [['bookTitle', 'totalRatingCount']]
    )
book_ratingCount.head()


rating_with_totalRatingCount = combine_book_rating.merge(book_ratingCount,
                                left_on = 'bookTitle', right_on = 'bookTitle', how = 'left')
rating_with_totalRatingCount.head()


pd.set_option('display.float_format', lambda x: '%.3f' % x)
print(book_ratingCount['totalRatingCount'].describe())


print(book_ratingCount['totalRatingCount'].quantile(np.arange(.9, 1, .01)))


popularity_threshold = 50
rating_popular_book = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
rating_popular_book.head()



combined = rating_popular_book.merge(users, left_on = 'userID', right_on = 'userID', how = 'left')

us_canada_user_rating = combined[combined['Location'].str.contains("usa|canada")]
us_canada_user_rating=us_canada_user_rating.drop('Age', axis=1)
us_canada_user_rating.head()


#svd matrix factorization
us_canada_user_rating = us_canada_user_rating.drop_duplicates(['userID', 'bookTitle'])
us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'userID', columns = 'bookTitle',
                                                          values = 'bookRating').fillna(0)
us_canada_user_rating_pivot.head()

us_canada_user_rating_pivot.shape
X = us_canada_user_rating_pivot.values.T
X.shape


from sklearn.decomposition import TruncatedSVD

SVD = TruncatedSVD(n_components=12, random_state=17)
matrix = SVD.fit_transform(X)
matrix.shape
import warnings
warnings.filterwarnings("ignore",category =RuntimeWarning)
corr = np.corrcoef(matrix)
corr.shape
us_canada_book_title = us_canada_user_rating_pivot.columns
us_canada_book_list = list(us_canada_book_title)



def valid():
    print(a1.get,",",b1.get)
    
  
    def rec():
        book=cb.get()
        coffey_hands = us_canada_book_list.index(book)
        #print(coffey_hands)
        corr_coffey_hands  = corr[coffey_hands]
        r=list(us_canada_book_title[(corr_coffey_hands>=0.90)])
        if len(r)<3:
            r=list(us_canada_book_title[(corr_coffey_hands>=0.75)])
        elif len(r)>7 and len(r)<=12:
            r=list(us_canada_book_title[(corr_coffey_hands>=0.80)])
        elif len(r)>12 and len(r)<=15:
            r=list(us_canada_book_title[(corr_coffey_hands>=0.85)])
        elif len(r)>15 and len(r)<=18:
            r=list(us_canada_book_title[(corr_coffey_hands>=0.90)])
        elif len(r)>19:
            r=list(us_canada_book_title[(corr_coffey_hands>=0.93)])
        
        
        
        fr=Frame(m,height=30)
        fr.place(x=270,y=150)
   
        lb=Listbox(fr,width=60,height=20)
        lb.pack(side=LEFT,fill=Y)
        lb.config(bg='black',fg='white')
        lb.config(font='Times 12 bold italic')
        sb=Scrollbar(fr,orient='vertical',command=lb.yview)
        sb.pack(side=RIGHT,fill=Y)
        lb.config(yscrollcommand=sb.set)
        for i in range(len(r)):
            lb.insert(i,r[i])
        
            '''books_out['text']=books_out['text']+'\n'+r[i]
            books_out.place(x=300,y=120)'''
            '''if(book!=''):
                cb1=Combobox(m,values=r,state='readonly',width=70)
                cb1.place(x=400,y=120)
                cb1.current(0)'''
    if(a1.get()=="Admin" and b1.get()=="admin"):  
    
        m=Tk()
        m.title('Book Recommendation')
        m.configure(background='grey')
        m.geometry("900x600")
        m.resizable(False,False)


        cb=Combobox(m,values=us_canada_book_list,state='readonly',width=75,font=('Times',10))
        cb.place(x=180,y=110)
        cb.current(0)

        l1=Label(m,text='Book Recommender')
        l1.config(bg='grey',fg='gold')
        l1.config(font='Times 20 bold italic')
        l1.place(x=350,y=30)



        last=Button(m,text='Get Recommended',command=rec,padx=60,pady=6)
        last.config(bg='gold',fg='purple')
        last.config(font='Times 7 bold italic')
        last.place(x=670,y=110)
        
       
        m.mainloop()
    else:
        c=Label(ma,text="password or username entered is incorrect")
        c.place(x=100,y=300)
        c.config(bg='grey',fg='white')

ma=Tk()

ma.geometry("500x500")
ma.title("Book Recommender-Login")
ma.configure(background='grey')
ma.resizable(False,False)
a=Label(ma,text="username")
a.place(x=100,y=100)
a.config(bg='grey',fg='white')
a1=Entry(ma)
a1.place(x=170,y=100)
b=Label(ma,text="password")
b.place(x=100,y=120)
b.config(bg='grey',fg='white')
b1=Entry(ma,show='*')
b1.place(x=170,y=120)
bt=Button(ma,text="Login",command=valid).place(x=200,y=200)
  
ma.mainloop()
       


'''   
m=Tk()
m.title('Book Recommendation')
m.configure(background='grey')
m.geometry("900x600")
m.resizable(False,False)


cb=Combobox(m,values=us_canada_book_list,state='readonly',width=75,font=('Times',10))
cb.place(x=180,y=110)
cb.current(0)

l1=Label(m,text='Book Recommender')
l1.config(bg='grey',fg='gold')
l1.config(font='Times 20 bold italic')
l1.place(x=350,y=30)



last=Button(m,text='Get Recommended',command=rec,padx=60,pady=6)
last.config(bg='gold',fg='purple')
last.config(font='Times 7 bold italic')
last.place(x=670,y=110)




m.mainloop()'''