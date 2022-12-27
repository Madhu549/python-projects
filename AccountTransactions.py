class Account:
  def __init__(self,acc_holder_name, acc_balance):
    self.acc_holder_name = acc_holder_name
    self.acc_balance = acc_balance

  def deposit(self,ammount):
    print(f'Current ammount is {self.acc_balance+ammount} rupees.')
    self.acc_balance += ammount
  def withdrawal(self,withdrawal_ammount):

    if withdrawal_ammount<=self.acc_balance:
      self.acc_balance -= withdrawal_ammount
      print(f'{withdrawal_ammount} rupees has been debited from your account and the remaining ammount is {self.acc_balance} rupees.')
    else:
      print('No sufficient balance in your account, Please enter another ammount')

  def __str__(self):
    return (f'{self.acc_holder_name} has {self.acc_balance} rupees in his Account.')
 

obj = Account(input('Enter Account holder name:'),int(input("Enter account balance: ")))
print(obj)
obj.deposit(int(input('Enter ammount to be credited: ')))
obj.withdrawal(int(input('Enter ammount to be debited: ')))
