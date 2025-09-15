def load_data(self):
    self.logger.info("Загрузка данных...")
    if os.path.exists(self.DATA_FILE):
        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.balance = decimal.Decimal(data.get("balance", "0.00"))
                self.transactions = [
                    Transaction(
                        transaction_id=t["id"],
                        amount=decimal.Decimal(t["amount"]),
                        transaction_type=TransactionType(t["type"]),
                        description=t["description"],
                        date=datetime.datetime.fromisoformat(t["date"]),
                        category=t.get("category", ""),
                        payer=t.get("payer", ""),
                        receiver=t.get("receiver", "")
                    ) for t in data.get("transactions", [])
                ]
            self.logger.info("Данные успешно загружены")
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке данных: {str(e)}")

def save_data(self):
    self.logger.info("Сохранение данных...")
    save_data = {
        "balance": str(self.balance),
        "transactions": [
            {
                "id": t.transaction_id,
                "amount": str(t.amount),
                "type": t.transaction_type.value,
                "description": t.description,
                "date": t.date.isoformat(),
                "category": t.category,
                "payer": t.payer,
                "receiver": t.receiver
            } for t in self.transactions
        ]
    }
    try:
        with open(self.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)
        self.logger.info("Данные успешно сохранены")
    except Exception as e:
        self.logger.error(f"Ошибка при сохранении данных: {str(e)}")

def delete_transaction(self, transaction_id: str) -> bool:
    self.logger.info(f"Удаление транзакции {transaction_id}")
    for transaction in self.transactions:
        if transaction.transaction_id == transaction_id:
            self.transactions.remove(transaction)
            self.update_balance(transaction, reverse=True)
            self.save_data()
            self.logger.info(f"Транзакция {transaction_id} удалена")
            return True
    self.logger.warning(f"Транзакция {transaction_id} не найдена")
    return False

def update_transaction(self, transaction_id: str, **kwargs) -> bool:
    self.logger.info(f"Обновление транзакции {transaction_id}")
    for transaction in self.transactions:
        if transaction.transaction_id == transaction_id:
            old_amount = transaction.amount
            for key, value in kwargs.items():
                if hasattr(transaction, key):
                    setattr(transaction, key, value)
            if "amount" in kwargs:
                new_amount = decimal.Decimal(str(kwargs["amount"]))
                self.balance += new_amount - old_amount
                transaction.amount = new_amount
                self.save_data()
                self.logger.info(f"Транзакция {transaction_id} обновлена")
                return True
    self.logger.warning(f"Транзакция {transaction_id} не найдена")
    return False